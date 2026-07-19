import os
import json
from pathlib import Path
from typing import Dict, Any

class CalculatorService:
    def __init__(self):
        # Load configuration
        config_path = Path(__file__).resolve().parent.parent / "core" / "calculator_config.json"
        if config_path.exists():
            with open(config_path, "r") as f:
                self.config = json.load(f)
        else:
            # Fallback defaults if configuration file is not found
            self.config = {
                "states_config": {
                    "default": 120.0,
                    "maharashtra": 120.0,
                    "gujarat": 125.0,
                    "rajasthan": 130.0,
                    "karnataka": 120.0,
                    "tamil nadu": 122.0,
                    "telangana": 120.0,
                    "delhi": 115.0
                },
                "cost_per_kw": {
                    "rooftop": 55000.0,
                    "ground-mount": 48000.0,
                    "on-grid": 55000.0,
                    "off-grid": 65000.0,
                    "hybrid": 75000.0
                },
                "subsidy_config": {
                    "residential_rooftop": {
                        "slabs": [
                            {"limit": 2.0, "rate": 30000.0},
                            {"limit": 3.0, "rate": 18000.0}
                        ],
                        "max_subsidy": 78000.0
                    }
                },
                "default_tariff": 7.0,
                "degradation_rate": 0.005,
                "co2_factor": 0.82,
                "area_per_kw": 100  # sq ft per kW
            }

    def calculate(
        self,
        # Customer
        customer_type: str,
        name: str,
        email: str,
        phone: str,
        pin_code: str | None,
        city: str | None,
        state: str | None,
        
        # Energy
        input_method: str,
        monthly_bill: float,
        monthly_units: float,
        tariff: float,
        connection_type: str,
        sanctioned_load: float | None,
        
        # Site
        property_type: str,
        roof_type: str,
        available_area: float,
        site_address: str | None,
        site_pin_code: str | None,
        site_city: str | None,
        site_state: str | None,
        latitude: float,
        longitude: float,
        
        # System
        system_type: str,
        panel_tech: str | None,
        system_loss_percent: float,
        inverter_efficiency: float,
        battery_storage: float | None,
        auto_recommend: bool,
        user_preferred_capacity: float | None,
        
        # Financial
        cost_per_kw: float,
        annual_tariff_escalation: float,
        om_cost: float,
        annual_om_escalation: float,
        panel_degradation: float,
        project_life: int,
        discount_rate: float,
        financing_type: str,
        down_payment: float | None,
        loan_amount: float | None,
        interest_rate: float | None,
        loan_tenure: int | None
    ) -> Dict[str, Any]:
        
        # State-based solar irradiance factor
        state_key = (state or site_state or "default").strip().lower()
        states_cfg = self.config.get("states_config", {})
        units_per_kw_per_month = states_cfg.get(state_key, states_cfg.get("default", 120.0))
        
        # Calculate recommended system size
        if auto_recommend or not user_preferred_capacity:
            required_system_size_kw = monthly_units / units_per_kw_per_month
        else:
            required_system_size_kw = user_preferred_capacity
        
        # Apply system and inverter efficiencies
        system_loss_factor = (100 - system_loss_percent) / 100.0
        inverter_efficiency_factor = inverter_efficiency / 100.0
        effective_system_size = required_system_size_kw * system_loss_factor * inverter_efficiency_factor
        
        # Annual generation
        annual_generation_kwh = effective_system_size * units_per_kw_per_month * 12
        
        # Area required
        area_per_kw = self.config.get("area_per_kw", 100)
        estimated_area_required = required_system_size_kw * area_per_kw
        
        # Cost per kW based on system type
        cost_per_kw_cfg = self.config.get("cost_per_kw", {})
        if cost_per_kw_cfg.get(system_type):
            cost_per_kw_final = cost_per_kw_cfg[system_type]
        else:
            cost_per_kw_final = cost_per_kw
            
        # Gross cost
        gross_cost = required_system_size_kw * cost_per_kw_final
        
        # Subsidy calculation (only for residential rooftop on-grid)
        subsidy_amount = 0.0
        if system_type == "on-grid" and property_type.lower() == "residential":
            subsidy_cfg = self.config.get("subsidy_config", {}).get("residential_rooftop", {})
            slabs = subsidy_cfg.get("slabs", [])
            max_subsidy = subsidy_cfg.get("max_subsidy", 78000.0)
            
            remaining_size = required_system_size_kw
            last_limit = 0.0
            for slab in slabs:
                limit = slab["limit"]
                rate = slab["rate"]
                slab_width = limit - last_limit
                
                if remaining_size <= 0:
                    break
                
                active_size = min(remaining_size, slab_width)
                subsidy_amount += active_size * rate
                remaining_size -= active_size
                last_limit = limit
                
            subsidy_amount = min(subsidy_amount, max_subsidy)
        
        # Net cost
        net_cost = max(0.0, gross_cost - subsidy_amount)
        
        # Annual cost before solar
        annual_cost_before_solar = monthly_units * tariff * 12
        
        # Annual cost after solar
        grid_units_used = max(0, (monthly_units * 12) - annual_generation_kwh)
        annual_cost_after_solar = grid_units_used * tariff
        
        # Annual and monthly savings
        annual_savings = max(0, annual_cost_before_solar - annual_cost_after_solar)
        monthly_savings = annual_savings / 12
        
        # Payback period
        payback_years = 0.0
        if annual_savings > 0:
            payback_years = net_cost / annual_savings
        
        # Lifetime calculations
        lifetime_savings_25yr = 0.0
        cumulative_cost_no_solar = 0.0
        cumulative_cost_with_solar = net_cost
        year_by_year = []
        
        deg_rate = panel_degradation / 100.0
        disc_rate = discount_rate / 100.0
        
        for year in range(1, 26):
            deg_factor = (1 - deg_rate) ** (year - 1)
            yearly_gen = annual_generation_kwh * deg_factor
            
            yearly_grid_usage = max(0, (monthly_units * 12) - yearly_gen)
            tariff_escalation = (1 + annual_tariff_escalation/100.0) ** (year - 1)
            yearly_cost_no_solar = (monthly_units * 12) * tariff * tariff_escalation
            yearly_cost_with_solar = yearly_grid_usage * tariff * tariff_escalation
            
            om_escalation = (1 + annual_om_escalation/100.0) ** (year -1)
            yearly_om_cost = om_cost * om_escalation
            
            yearly_cost_with_solar += yearly_om_cost
            
            yearly_savings = yearly_cost_no_solar - yearly_cost_with_solar
            
            if year <= project_life:
                cumulative_cost_no_solar += yearly_cost_no_solar
                cumulative_cost_with_solar += yearly_cost_with_solar
                lifetime_savings_25yr += yearly_savings
                
                year_by_year.append({
                    "year": year,
                    "cost_no_solar": round(yearly_cost_no_solar, 2),
                    "cost_with_solar": round(yearly_cost_with_solar, 2),
                    "savings": round(yearly_savings, 2)
                })
        
        # ROI
        roi = 0.0
        if net_cost > 0:
            roi = (lifetime_savings_25yr / net_cost) * 100
        
        # NPV (simple)
        npv = -net_cost
        for i, yy in enumerate(year_by_year):
            npv += yy["savings"] / (1 + disc_rate) ** (i+1)
        
        # LCOE
        total_generation = sum([annual_generation_kwh * ((1-deg_rate)**y) for y in range(25)])
        lcoe = cumulative_cost_with_solar / total_generation if total_generation > 0 else 0
        
        # Carbon offset
        co2_factor = self.config.get("co2_factor", 0.82)
        co2_offset_kg = annual_generation_kwh * co2_factor
        
        # Data quality
        dq_score = 0
        dq_reasons = []
        
        if tariff > 0:
            dq_score += 30
            dq_reasons.append("Valid tariff provided")
        if latitude != 0 and longitude !=0:
            dq_score +=30
            dq_reasons.append("Valid location selected")
        if available_area >0:
            dq_score +=20
            dq_reasons.append("Available area provided")
        if phone and len(phone)>=10:
            dq_score +=10
            dq_reasons.append("Contact details complete")
        if monthly_units>0:
            dq_score +=10
            dq_reasons.append("Energy consumption provided")
        
        data_quality_score = min(100, dq_score)
        
        # Recommendations
        recs = []
        if estimated_area_required > available_area:
            recs.append({"type": "warning", "text": "Insufficient available space for recommended system size"})
        if payback_years > 8:
            recs.append({"type": "info", "text": "Consider long-term financing options"})
        if data_quality_score <50:
            recs.append({"type": "info", "text": "Provide more data for better accuracy"})
        
        # Round results
        return {
            "customer_type": customer_type,
            "name": name,
            "email": email,
            "phone": phone,
            "pin_code": pin_code,
            "city": city,
            "state": state,
            
            "input_method": input_method,
            "monthly_bill": round(monthly_bill, 2),
            "monthly_units": round(monthly_units, 1),
            "tariff": round(tariff, 2),
            "connection_type": connection_type,
            "sanctioned_load": sanctioned_load,
            
            "property_type": property_type,
            "roof_type": roof_type,
            "available_area": available_area,
            "site_address": site_address,
            "site_pin_code": site_pin_code,
            "site_city": site_city,
            "site_state": site_state,
            "latitude": latitude,
            "longitude": longitude,
            
            "system_type": system_type,
            "panel_tech": panel_tech,
            "system_loss_percent": system_loss_percent,
            "inverter_efficiency": inverter_efficiency,
            "battery_storage": battery_storage,
            "auto_recommend": auto_recommend,
            "user_preferred_capacity": user_preferred_capacity,
            
            "cost_per_kw": cost_per_kw_final,
            "annual_tariff_escalation": annual_tariff_escalation,
            "om_cost": om_cost,
            "annual_om_escalation": annual_om_escalation,
            "panel_degradation": panel_degradation,
            "project_life": project_life,
            "discount_rate": discount_rate,
            "financing_type": financing_type,
            "down_payment": down_payment,
            "loan_amount": loan_amount,
            "interest_rate": interest_rate,
            "loan_tenure": loan_tenure,
            
            "calculated_system_size_kw": round(required_system_size_kw, 2),
            "estimated_area_required": round(estimated_area_required, 1),
            "annual_generation_kwh": round(annual_generation_kwh, 0),
            "estimated_cost": round(gross_cost, -2),
            "subsidy_amount": round(subsidy_amount, -2),
            "net_cost": round(net_cost, -2),
            "annual_cost_before_solar": round(annual_cost_before_solar, -2),
            "annual_cost_after_solar": round(annual_cost_after_solar, -2),
            "annual_savings": round(annual_savings, -2),
            "monthly_savings": round(monthly_savings, -2),
            "payback_years": round(payback_years, 1),
            "lifetime_savings_25yr": round(lifetime_savings_25yr, -2),
            "roi": round(roi, 1) if roi else None,
            "npv": round(npv, -2) if npv else None,
            "irr": None,
            "lcoe": round(lcoe, 3) if lcoe else None,
            "co2_offset_kg": round(co2_offset_kg, 1),
            "data_quality_score": data_quality_score,
            "recommendations": recs
        }

calculator_service = CalculatorService()
