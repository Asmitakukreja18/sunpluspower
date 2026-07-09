import os
import sys
from datetime import datetime, date

# Add the parent directory to sys.path so we can import app modules
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.core.db import SessionLocal
from app.models.models import Project, Career, Blog, Event, Gallery

def seed():
    db = SessionLocal()
    try:
        # Clear existing test projects/careers to avoid duplication
        db.query(Project).delete()
        db.query(Career).delete()
        db.query(Blog).delete()
        db.query(Event).delete()
        db.query(Gallery).delete()
        db.commit()
        print("Cleared existing projects, careers, blogs, events, and gallery data.")

        # 1. Seed Projects
        projects = [
            Project(
                name="Manjari Project",
                capacity_mw=8.4,
                location="Manjari, Solapur",
                state="Maharashtra",
                status="operational",
                commissioning_date=date(2023, 11, 12),
                description="Industrial scale solar plant engineering with high-performance tracking arrays for peak yield.",
                image_url="https://images.unsplash.com/photo-1509391366360-2e959784a276"
            ),
            Project(
                name="Achakdani Project",
                capacity_mw=8.4,
                location="Achakdani",
                state="Maharashtra",
                status="operational",
                commissioning_date=date(2023, 8, 20),
                description="High-voltage substation integration and balanced-of-system design for industrial power supplies.",
                image_url="https://images.unsplash.com/photo-1508514177221-188b1cf16e9d"
            ),
            Project(
                name="Gherdi Project",
                capacity_mw=8.4,
                location="Gherdi, Sangli",
                state="Maharashtra",
                status="operational",
                commissioning_date=date(2023, 5, 15),
                description="Grid-interactive solar array optimization featuring premium monocrystalline modules.",
                image_url="https://images.unsplash.com/photo-1473341304170-971dccb5ac1e"
            ),
            Project(
                name="Watambare Project",
                capacity_mw=6.0,
                location="Watambare",
                state="Maharashtra",
                status="operational",
                commissioning_date=date(2022, 12, 10),
                description="Engineering execution of grid-tied infrastructure for municipal utility scaling.",
                image_url="https://images.unsplash.com/photo-1548613053-22070f317698"
            ),
            Project(
                name="Ambora Project",
                capacity_mw=8.0,
                location="Ambora",
                state="Maharashtra",
                status="operational",
                commissioning_date=date(2022, 9, 5),
                description="Strategic substation connectivity and structural design under complex land topography.",
                image_url="https://images.unsplash.com/photo-1509391366360-2e959784a276"
            ),
            Project(
                name="Kuhi Project",
                capacity_mw=6.0,
                location="Kuhi, Nagpur",
                state="Maharashtra",
                status="operational",
                commissioning_date=date(2022, 4, 18),
                description="Operations and maintenance hub deployment for continuous generation yields.",
                image_url="https://images.unsplash.com/photo-1508514177221-188b1cf16e9d"
            ),
            Project(
                name="Pachkhedi Project",
                capacity_mw=9.0,
                location="Pachkhedi",
                state="Maharashtra",
                status="operational",
                commissioning_date=date(2021, 10, 25),
                description="High-capacity utility solar installation supporting regional transmission networks.",
                image_url="https://images.unsplash.com/photo-1473341304170-971dccb5ac1e"
            ),
            Project(
                name="Asti Project",
                capacity_mw=3.6,
                location="Asti, Beed",
                state="Maharashtra",
                status="operational",
                commissioning_date=date(2021, 6, 30),
                description="Precision ground-mounted system with localized net-metering synchronization.",
                image_url="https://images.unsplash.com/photo-1548613053-22070f317698"
            ),
            Project(
                name="Bhose Project",
                capacity_mw=4.8,
                location="Bhose",
                state="Maharashtra",
                status="operational",
                commissioning_date=date(2021, 2, 14),
                description="Early-stage solar deployment optimizing local balance-of-system efficiencies.",
                image_url="https://images.unsplash.com/photo-1509391366360-2e959784a276"
            )
        ]
        for p in projects:
            db.add(p)
        print(f"Added {len(projects)} projects.")

        # 2. Seed Careers
        careers = [
            Career(
                title="Solar Design Engineer",
                department="Design & Engineering",
                location="Lucknow, UP",
                experience_required="3-5 Years",
                description="Lead utility-scale PV system layouts, SLD diagrams, and energy yield simulations using PVSyst.",
                is_active=True
            ),
            Career(
                title="Project Operations Manager",
                department="EPC",
                location="Lucknow, UP",
                experience_required="5-8 Years",
                description="Coordinate end-to-end onsite solar plant installations, resource allocation, and utility compliance.",
                is_active=True
            ),
            Career(
                title="Grid Integration Specialist",
                department="Balance of System",
                location="Gomti Nagar, Lucknow",
                experience_required="4+ Years",
                description="Supervise solar substation commissioning, transformer testing, and state load dispatch center sync.",
                is_active=True
            )
        ]
        for c in careers:
            db.add(c)
        print(f"Added {len(careers)} careers.")

        # 3. Seed Blogs
        blogs = [
            Blog(
                title="The Growth of Industrial Solar in Uttar Pradesh",
                slug="growth-industrial-solar-up",
                excerpt="Uttar Pradesh is witnessing a boom in solar. Let's look at the growth vectors.",
                content="Industrial scale power systems are revolutionizing energy independence in North India. Discover tariff benefits, state policies, and net-metering advantages.",
                author="Sunil Sagar",
                cover_image_url="https://images.unsplash.com/photo-1509391366360-2e959784a276",
                published=True,
                published_at=datetime.utcnow()
            ),
            Blog(
                title="Operation & Maintenance Best Practices for Megawatt Plants",
                slug="om-best-practices-mw-plants",
                excerpt="Explore best practices to improve megawatt scale uptime.",
                content="Thermal imaging, regular array cleanings, and automated SCADA alerts ensure optimal uptime for industrial utility solar networks.",
                author="Raghuveer Prasad",
                cover_image_url="https://images.unsplash.com/photo-1508514177221-188b1cf16e9d",
                published=True,
                published_at=datetime.utcnow()
            )
        ]
        for b in blogs:
            db.add(b)
        print(f"Added {len(blogs)} blogs.")

        # 4. Seed Events
        events = [
            Event(
                title="Solar Grid Integration Summit 2026",
                location="Indira Gandhi Pratishthan, Lucknow",
                event_date=date(2026, 10, 15),
                description="SunPlus Power joins state regulators and utility leads to align grid safety and performance metrics.",
                image_url="https://images.unsplash.com/photo-1548613053-22070f317698"
            ),
            Event(
                title="Uttar Pradesh Renewable Energy Expo",
                location="Vibhuti Khand, Lucknow",
                event_date=date(2026, 7, 20),
                description="Showcasing high-efficiency monocrystalline modules and smart solar tracking systems.",
                image_url="https://images.unsplash.com/photo-1473341304170-971dccb5ac1e"
            )
        ]
        for e in events:
            db.add(e)
        print(f"Added {len(events)} events.")

        # 5. Seed Gallery
        gallery_items = [
            Gallery(caption="Solar Array Overhead View", category="om", image_url="https://images.unsplash.com/photo-1509391366360-2e959784a276"),
            Gallery(caption="Substation Transformer Setup", category="infrastructure", image_url="https://images.unsplash.com/photo-1508514177221-188b1cf16e9d"),
            Gallery(caption="Engineering Site Assessment", category="rooftop", image_url="https://images.unsplash.com/photo-1548613053-22070f317698")
        ]
        for g in gallery_items:
            db.add(g)
        print(f"Added {len(gallery_items)} gallery items.")

        db.commit()
        print("Database successfully seeded!")
    except Exception as err:
        db.rollback()
        print(f"Failed to seed data: {err}")
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    seed()
