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
                    "ground-mount": 48000.0
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
                "co2_factor": 0.82
            }

    def calculate(
        self,
        name: str,
        email: str,
        phone: str | None,
        monthly_bill: float,
        monthly_units: float | None,
        location: str,
        install_type: str
    ) -> Dict[str, Any]:
        
        # 1. Determine unit tariff and estimate monthly units if not provided
        per_unit_tariff = self.config.get("default_tariff", 7.0)
        if not monthly_units or monthly_units <= 0:
            monthly_units = monthly_bill / per_unit_tariff

        # 2. State-based solar irradiance factor
        state_key = location.strip().lower()
        states_cfg = self.config.get("states_config", {})
        units_per_kw_per_month = states_cfg.get(state_key, states_cfg.get("default", 120.0))

        # 3. Required system size in kW
        required_system_size_kw = monthly_units / units_per_kw_per_month

        # 4. Cost per kW based on install type
        cost_per_kw_cfg = self.config.get("cost_per_kw", {})
        cost_per_kw = cost_per_kw_cfg.get(install_type, 55000.0)

        # 5. Gross cost
        gross_cost = required_system_size_kw * cost_per_kw

        # 6. Subsidy calculation (only for rooftop systems)
        subsidy_amount = 0.0
        if install_type == "rooftop":
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

        # 7. Net cost
        net_cost = max(0.0, gross_cost - subsidy_amount)

        # 8. Annual generation units (kWh)
        annual_generation_units = required_system_size_kw * units_per_kw_per_month * 12

        # 9. Annual savings
        annual_savings = annual_generation_units * per_unit_tariff

        # 10. Payback period in years
        payback_years = 0.0
        if annual_savings > 0:
            payback_years = net_cost / annual_savings

        # 11. Lifetime savings over 25 years with ~0.5% annual degradation
        degradation_rate = self.config.get("degradation_rate", 0.005)
        cumulative_savings = 0.0
        for year in range(1, 26):
            deg_factor = (1.0 - degradation_rate) ** (year - 1)
            yearly_savings = (annual_generation_units * deg_factor) * per_unit_tariff
            cumulative_savings += yearly_savings
            
        lifetime_savings_25yr = cumulative_savings - net_cost

        # 12. Carbon offset in kg CO2 per year
        co2_factor = self.config.get("co2_factor", 0.82)
        co2_offset_kg = annual_generation_units * co2_factor

        # Round results
        return {
            "name": name,
            "email": email,
            "phone": phone,
            "monthly_bill": round(monthly_bill, 2),
            "monthly_units": round(monthly_units, 1),
            "location": location,
            "install_type": install_type,
            "calculated_system_size_kw": round(required_system_size_kw, 2),
            "estimated_cost": round(gross_cost, -2),  # Round to nearest ₹100
            "subsidy_amount": round(subsidy_amount, -2),
            "net_cost": round(net_cost, -2),
            "annual_savings": round(annual_savings, -2),
            "payback_years": round(payback_years, 1),
            "lifetime_savings_25yr": round(lifetime_savings_25yr, -2),
            "co2_offset_kg": round(co2_offset_kg, 1)
        }

calculator_service = CalculatorService()
