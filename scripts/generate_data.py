"""Generate synthetic single-family rental (SFR) data for the Tricon CoCo HOL.

All data is fictional. Markets mirror a Sun Belt SFR footprint; no Tricon or
resident data is used. Run from the repo root:  python scripts/generate_data.py
"""
import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(1109)
OUT = Path(__file__).resolve().parent.parent / "workshop_guide" / "data"
OUT.mkdir(parents=True, exist_ok=True)


def write(name, header, rows):
    with open(OUT / f"{name}.csv", "w", newline="") as f:
        w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        w.writerow(header)
        w.writerows(rows)
    print(f"{name}: {len(rows)} rows")


def rand_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))


# --- MARKETS (dimension) -------------------------------------------------
MARKETS = [
    ("MKT01", "Atlanta", "GA", "Southeast", 2013, 1650),
    ("MKT02", "Charlotte", "NC", "Southeast", 2013, 1700),
    ("MKT03", "Phoenix", "AZ", "Southwest", 2012, 1850),
    ("MKT04", "Tampa", "FL", "Florida", 2014, 1950),
    ("MKT05", "Dallas-Fort Worth", "TX", "Texas", 2015, 1800),
    ("MKT06", "Houston", "TX", "Texas", 2015, 1650),
    ("MKT07", "Nashville", "TN", "Southeast", 2016, 1900),
    ("MKT08", "Raleigh", "NC", "Southeast", 2017, 1750),
    ("MKT09", "Jacksonville", "FL", "Florida", 2016, 1700),
    ("MKT10", "Orlando", "FL", "Florida", 2017, 1900),
    ("MKT11", "Las Vegas", "NV", "Southwest", 2014, 1800),
    ("MKT12", "Columbia", "SC", "Southeast", 2018, 1450),
    ("MKT13", "Indianapolis", "IN", "Midwest", 2015, 1450),
    ("MKT14", "Southeast Florida", "FL", "Florida", 2019, 2600),
]
write("markets",
      ["MARKET_ID", "MARKET_NAME", "STATE", "REGION", "ENTRY_YEAR",
       "TARGET_OCCUPANCY_PCT", "BASE_MARKET_RENT"],
      [(m[0], m[1], m[2], m[3], m[4], random.choice([95.0, 95.5, 96.0, 96.5]), m[5])
       for m in MARKETS])
BASE_RENT = {m[0]: m[5] for m in MARKETS}
CITY_BY_MARKET = {
    "MKT01": ["Marietta", "Lawrenceville", "Kennesaw", "Snellville"],
    "MKT02": ["Concord", "Matthews", "Huntersville", "Gastonia"],
    "MKT03": ["Mesa", "Gilbert", "Chandler", "Glendale"],
    "MKT04": ["Brandon", "Riverview", "Wesley Chapel", "Clearwater"],
    "MKT05": ["Frisco", "McKinney", "Mesquite", "Arlington"],
    "MKT06": ["Katy", "Cypress", "Pearland", "Spring"],
    "MKT07": ["Murfreesboro", "Antioch", "Hendersonville", "Smyrna"],
    "MKT08": ["Cary", "Wake Forest", "Garner", "Apex"],
    "MKT09": ["Orange Park", "Fleming Island", "Yulee", "Mandarin"],
    "MKT10": ["Kissimmee", "Clermont", "Sanford", "Apopka"],
    "MKT11": ["Henderson", "North Las Vegas", "Summerlin", "Enterprise"],
    "MKT12": ["Lexington", "Irmo", "Blythewood", "West Columbia"],
    "MKT13": ["Fishers", "Avon", "Greenwood", "Noblesville"],
    "MKT14": ["Port St. Lucie", "Homestead", "Boynton Beach", "Davie"],
}
STREETS = ["Oak Hollow Dr", "Magnolia Ct", "Cedar Ridge Ln", "Willow Bend Way",
           "Pine Meadow Rd", "Sunset Trail", "Hickory Grove Ct", "Desert Sage Ave",
           "Palm Harbor Blvd", "Bluebonnet Ln", "Riverstone Dr", "Laurel Park Pl",
           "Juniper Springs Rd", "Heritage Oaks Dr", "Cypress Point Ln"]

# --- PROPERTIES (dimension) ----------------------------------------------
properties = []
for i in range(1, 121):
    mkt = MARKETS[(i - 1) % len(MARKETS)][0]
    beds = random.choices([3, 4, 5], weights=[50, 40, 10])[0]
    baths = {3: random.choice([2.0, 2.5]), 4: random.choice([2.5, 3.0]), 5: 3.5}[beds]
    sqft = beds * 450 + random.randint(-150, 400)
    acq = rand_date(date(2014, 1, 1), date(2024, 6, 30))
    price = round(sqft * random.uniform(140, 235) * (BASE_RENT[mkt] / 1750), -3)
    status = random.choices(["Occupied", "Vacant - Make Ready", "Vacant - Listed", "Pending Disposition"],
                            weights=[86, 6, 6, 2])[0]
    properties.append((f"P{i:04d}", mkt,
                       f"{random.randint(100, 9899)} {random.choice(STREETS)}",
                       random.choice(CITY_BY_MARKET[mkt]), MARKETS[(i - 1) % 14][2],
                       beds, baths, sqft, random.randint(1996, 2021),
                       acq.isoformat(), int(price),
                       random.choice(["Scattered Site", "Scattered Site", "Build-to-Rent Community"]),
                       status))
write("properties",
      ["PROPERTY_ID", "MARKET_ID", "ADDRESS", "CITY", "STATE", "BEDROOMS", "BATHROOMS",
       "SQUARE_FEET", "YEAR_BUILT", "ACQUISITION_DATE", "ACQUISITION_PRICE",
       "PROPERTY_TYPE", "PROPERTY_STATUS"], properties)
PROP_MKT = {p[0]: p[1] for p in properties}
PROP_SQFT = {p[0]: p[7] for p in properties}

# --- VENDORS (dimension) -------------------------------------------------
vendor_names = [
    ("Sun Belt HVAC Services", "HVAC"), ("ProFlow Plumbing", "Plumbing"),
    ("BrightLine Electric", "Electrical"), ("Greenway Lawn & Landscape", "Landscaping"),
    ("Apex Roofing Partners", "Roofing"), ("TurnKey Make-Ready Co", "Turnover / Make-Ready"),
    ("ShieldPest Solutions", "Pest Control"), ("Keystone Appliance Repair", "Appliances"),
    ("ClearView Glass & Doors", "Doors & Windows"), ("Summit General Contracting", "General Repair"),
    ("CoolBreeze Mechanical", "HVAC"), ("RapidRooter Drain Pros", "Plumbing"),
    ("FreshCoat Painting", "Turnover / Make-Ready"), ("Guardian Water Restoration", "Water Mitigation"),
    ("Precision Flooring Group", "Flooring"),
]
vendors = []
for i, (n, t) in enumerate(vendor_names, 1):
    vendors.append((f"V{i:03d}", n, t, random.choice(["National", "Southeast", "Texas", "Florida", "Southwest"]),
                    round(random.uniform(3.4, 4.9), 1), random.choice(["Y", "Y", "N"]),
                    random.choice([24, 48, 48, 72])))
write("vendors", ["VENDOR_ID", "VENDOR_NAME", "TRADE", "SERVICE_REGION", "QUALITY_RATING",
                  "PREFERRED_VENDOR", "SLA_HOURS"], vendors)
VENDORS_BY_TRADE = {}
for v in vendors:
    VENDORS_BY_TRADE.setdefault(v[2], []).append(v[0])

# --- LEASES (fact) -------------------------------------------------------
leases = []
for i in range(1, 201):
    pid = random.choice(properties)[0]
    start = rand_date(date(2024, 1, 1), date(2026, 9, 30))
    term = random.choices([12, 12, 12, 18, 24, 6], k=1)[0]
    end = start + timedelta(days=round(term * 30.4))
    rent = round(BASE_RENT[PROP_MKT[pid]] * (PROP_SQFT[pid] / 1700) ** 0.5 * random.uniform(0.92, 1.12) / 5) * 5
    ltype = random.choices(["Renewal", "New Lease"], weights=[62, 38])[0]
    growth = round(random.uniform(2.5, 6.5) if ltype == "Renewal" else random.uniform(-3.0, 8.0), 1)
    status = "Active" if end >= date(2026, 10, 26) else random.choice(["Expired - Renewed", "Expired - Moved Out", "Expired - Moved Out"])
    leases.append((f"L{i:05d}", pid, start.isoformat(), end.isoformat(), term, int(rent), ltype,
                   growth, random.choice(["A", "A", "B", "B", "C"]), int(rent) * random.choice([1, 1, 1.5]),
                   random.choice(["Y", "N", "N"]), status))
write("leases", ["LEASE_ID", "PROPERTY_ID", "LEASE_START_DATE", "LEASE_END_DATE", "TERM_MONTHS",
                 "MONTHLY_RENT", "LEASE_TYPE", "RENT_CHANGE_PCT", "RESIDENT_SCORE_BAND",
                 "SECURITY_DEPOSIT", "HAS_PET", "LEASE_STATUS"], leases)

# --- WORK_ORDERS (fact) --------------------------------------------------
WO_CATS = {
    "HVAC": (180, 1400), "Plumbing": (120, 950), "Electrical": (110, 800),
    "Landscaping": (60, 350), "Roofing": (400, 6500), "Turnover / Make-Ready": (1200, 7500),
    "Pest Control": (75, 300), "Appliances": (95, 1100), "Doors & Windows": (90, 900),
    "General Repair": (80, 1200), "Water Mitigation": (900, 9000), "Flooring": (600, 5200),
}
work_orders = []
for i in range(1, 301):
    pid = random.choice(properties)[0]
    cat = random.choices(list(WO_CATS), weights=[18, 15, 6, 6, 3, 14, 6, 10, 5, 10, 2, 5])[0]
    pri = random.choices(["Emergency", "Urgent", "Routine"], weights=[12, 28, 60])[0]
    opened = rand_date(date(2025, 1, 1), date(2026, 10, 15))
    days = {"Emergency": random.randint(0, 2), "Urgent": random.randint(1, 5), "Routine": random.randint(2, 18)}[pri]
    if cat == "Turnover / Make-Ready":
        days = random.randint(6, 24)
    done = opened + timedelta(days=days)
    status = "Completed" if done <= date(2026, 10, 20) else random.choice(["In Progress", "Scheduled"])
    lo, hi = WO_CATS[cat]
    cost = round(random.uniform(lo, hi), 2) if status == "Completed" else ""
    source = "Turnover" if cat == "Turnover / Make-Ready" else random.choice(["Resident Request", "Resident Request", "Inspection", "Preventive"])
    work_orders.append((f"WO{i:05d}", pid, random.choice(VENDORS_BY_TRADE[cat]), cat, pri, source,
                        opened.isoformat(), done.isoformat() if status == "Completed" else "",
                        days if status == "Completed" else "", cost, status,
                        random.choice([3, 4, 4, 5, 5, 5]) if status == "Completed" else ""))
write("work_orders", ["WORK_ORDER_ID", "PROPERTY_ID", "VENDOR_ID", "CATEGORY", "PRIORITY", "SOURCE",
                      "OPENED_DATE", "COMPLETED_DATE", "DAYS_TO_COMPLETE", "TOTAL_COST", "STATUS",
                      "RESIDENT_SATISFACTION"], work_orders)

# --- MARKET_MONTHLY_PERFORMANCE (time series) ----------------------------
perf = []
for m in MARKETS:
    homes = random.randint(380, 2100)
    occ = random.uniform(94.0, 97.5)
    rent = m[5] * 0.93
    for k in range(24):
        month = date(2024 + (9 + k) // 12, (9 + k) % 12 + 1, 1)
        season = 0.6 if month.month in (5, 6, 7, 8) else (-0.5 if month.month in (12, 1) else 0)
        occ = min(98.5, max(91.5, occ + random.uniform(-0.6, 0.6) + season * 0.3))
        rent *= 1 + random.uniform(0.0005, 0.0055)
        homes += random.randint(-4, 9)
        occupied = round(homes * occ / 100)
        turnover = max(3, round(homes * random.uniform(0.018, 0.034)))
        perf.append((m[0], month.isoformat(), homes, occupied, round(occupied / homes * 100, 2),
                     round(rent, 2), round(random.uniform(2.8, 6.2), 2), round(random.uniform(-2.5, 6.5), 2),
                     turnover, random.randint(19, 46), round(random.uniform(0.4, 1.9), 2),
                     round(random.uniform(74, 91), 1)))
write("market_monthly_performance",
      ["MARKET_ID", "MONTH", "TOTAL_HOMES", "OCCUPIED_HOMES", "OCCUPANCY_PCT", "AVG_MONTHLY_RENT",
       "RENEWAL_RENT_GROWTH_PCT", "NEW_LEASE_RENT_GROWTH_PCT", "MOVE_OUTS", "AVG_DAYS_TO_RELEASE",
       "BAD_DEBT_PCT", "RESIDENT_NPS_PROXY"], perf)

# --- RESIDENT_SERVICE_TICKETS (unstructured) -----------------------------
TICKETS = [
    ("HVAC", "Emergency", "Resident reported the AC stopped cooling overnight with the indoor temperature reaching 88 degrees. A toddler and an elderly parent live in the home, so the resident asked for same-day service.",
     "Technician found a failed capacitor and a clogged condensate line. Both were replaced and cleared, cooling was restored within 4 hours of dispatch, and a filter-change reminder was added to the resident portal."),
    ("HVAC", "Urgent", "The thermostat shows the system running, but upstairs bedrooms stay roughly 10 degrees warmer than the main floor. The resident says this is the third complaint since June.",
     "The vendor found disconnected supply ductwork in the attic and resealed it. The recurring complaint was flagged for a capital review of the 2004 air handler."),
    ("Plumbing", "Emergency", "Water is leaking from the ceiling below the upstairs bathroom and has stained the drywall in the living room. The resident shut off the bathroom supply valve but water continued to drip.",
     "The plumber traced the leak to a failed wax ring and a cracked supply line. A water mitigation vendor ran moisture readings and set dehumidifiers, and drywall repair was scheduled after a 72-hour dry-out."),
    ("Plumbing", "Urgent", "Kitchen sink drains slowly and backs up into the second basin when the dishwasher runs. The resident tried a store-bought drain cleaner with no improvement.",
     "Main kitchen line was snaked and roots were found at the cleanout. The resident was given guidance on avoiding chemical drain cleaners, which damage older PVC joints."),
    ("Plumbing", "Routine", "The water heater is producing lukewarm water for only about five minutes during morning showers. The household has five occupants.",
     "Lower heating element and thermostat were replaced on the 40-gallon unit. The technician recommended upsizing to 50 gallons at next turnover given occupancy."),
    ("Appliances", "Urgent", "The refrigerator is not keeping food cold and the freezer has begun to thaw. The resident asked whether spoiled groceries would be reimbursed.",
     "Compressor relay replaced same day. The resident was referred to the renter's insurance policy for food loss per the lease addendum, and the case was escalated to the community manager for a courtesy credit decision."),
    ("Appliances", "Routine", "The dishwasher leaves standing water at the bottom after each cycle and has developed a musty odor.",
     "The drain pump filter was clogged with debris and was cleaned. The unit is 11 years old and was tagged for replacement at the next turnover."),
    ("Pest Control", "Urgent", "Resident reported seeing several roaches in the kitchen and bathroom within one week of move-in. They are concerned the home was not treated before occupancy.",
     "An interior treatment was applied with a 30-day follow-up. The make-ready checklist for this property showed the pre-move-in pest treatment was skipped, and this was reported to the turnover vendor manager."),
    ("Pest Control", "Routine", "Fire ants are mounding along the driveway and in the backyard, where the resident's children play.",
     "A perimeter and yard granular treatment was applied. The property was added to the quarterly exterior pest program for Florida markets."),
    ("Electrical", "Emergency", "Outlets in the garage and one bathroom stopped working, and the resident smelled burning near the electrical panel.",
     "The electrician found a scorched breaker and a loose neutral connection and replaced the breaker. The home was inspected for additional hazards, and a GFCI outlet was installed in the bathroom to meet code."),
    ("Electrical", "Routine", "Two exterior light fixtures do not turn on and the resident is concerned about safety at night.",
     "Fixtures were replaced with LED dusk-to-dawn units, consistent with the portfolio exterior lighting standard."),
    ("Roofing", "Urgent", "After a heavy thunderstorm the resident noticed a brown water stain spreading on the bedroom ceiling. Shingles were found in the yard.",
     "The roofer tarped the damaged section within 24 hours and documented hail and wind damage. An insurance claim was opened, and the permanent repair was scheduled pending adjuster review."),
    ("Doors & Windows", "Routine", "The back sliding door is very hard to open and does not lock, which the resident considers a security problem.",
     "Rollers and track were replaced and the lock mechanism was realigned. The resident confirmed the door locks properly."),
    ("Landscaping", "Routine", "The HOA sent a violation notice for overgrown grass and dead shrubs in the front yard. The resident says landscaping is supposed to be included in their lease.",
     "The lease was confirmed to include monthly landscaping. The vendor had missed two visits, so service was performed and the HOA violation was resolved before a fine was assessed. A vendor scorecard deduction was logged."),
    ("General Repair", "Routine", "The garage door opener makes a grinding noise and stops halfway when closing.",
     "Drive gear and safety sensors were replaced. The resident received safe-operation instructions."),
    ("Water Mitigation", "Emergency", "A washing machine supply hose burst while the resident was at work, flooding the laundry room and hallway with roughly an inch of standing water.",
     "Extraction and drying equipment ran for 3 days. Laminate flooring in the hallway was removed and replaced. Braided steel supply hoses were installed and the portfolio standard was updated to require them."),
    ("Billing / Account", "Routine", "The resident disputes a $185 utility reimbursement charge and says the water bill shows usage while the home was vacant before move-in.",
     "The utility ledger confirmed the charge covered days before the lease start date. The charge was reversed, and the move-in utility transfer process was reviewed with the leasing team."),
    ("Billing / Account", "Urgent", "The resident received a late fee even though the rent payment was submitted through the portal on the 1st. The bank shows the payment as pending.",
     "The payment processor reported a settlement delay affecting 37 residents. Late fees were waived in bulk and a portal notification was sent."),
    ("Lease / Renewal", "Routine", "The resident received a renewal offer with a 7.5% increase and asked why it is higher than their neighbor's, who renewed at 4%.",
     "Revenue management explained that the renewal price reflects comparable listings for the home's size and finishes. A 12-month renewal at 5.25% was offered as a retention concession, and the resident accepted."),
    ("Lease / Renewal", "Routine", "The resident is relocating for work and asked about options to end their lease 4 months early without penalty.",
     "The early-termination policy was explained (60-day notice plus one month's rent), along with the option to transfer to a home in another market with no fee. The resident chose to transfer to the Nashville market."),
    ("HVAC", "Urgent", "Heat pump is blowing cold air on the heat setting and the auxiliary heat light stays on. Overnight lows are in the 30s.",
     "A reversing valve solenoid was replaced. The technician noted the outdoor unit was undersized for the square footage and flagged it for replacement planning."),
    ("Plumbing", "Routine", "The toilet in the hall bathroom runs continuously, and the resident is worried about their water bill.",
     "Flapper and fill valve replaced. A leak-detection sensor was offered and installed under the smart-home program."),
    ("Smart Home", "Routine", "The smart lock keypad stopped accepting the resident's code and they had to use the physical key.",
     "Batteries were replaced and the lock was re-paired with the hub. Codes were re-provisioned remotely through the smart home platform."),
    ("Smart Home", "Urgent", "The resident cannot connect the smart thermostat to their new Wi-Fi and the schedule has reset to default.",
     "Remote support walked the resident through re-pairing. The help article for Wi-Fi changes was updated because it is the most common smart-home ticket."),
    ("Mold / Moisture", "Urgent", "The resident sees black spotting on the bathroom ceiling and around the window frame and is worried about health effects for their child with asthma.",
     "An inspector found surface mold from poor ventilation; the exhaust fan was not venting outside. The fan was re-ducted to the exterior, a remediation vendor treated the area, and the resident was offered temporary lodging per the moisture policy."),
    ("Appliances", "Routine", "The oven takes over 40 minutes to preheat and the bake element visibly glows unevenly.",
     "Bake element replaced; oven temperature calibration verified."),
    ("Turnover", "Routine", "The new resident reported carpet stains in two bedrooms, a missing blind in the kitchen, and nail holes that were not patched after move-in.",
     "The move-in inspection photos confirmed the items were missed during make-ready. The turnover vendor returned within 48 hours at no cost, and the QA sign-off step was reinforced for the Atlanta market."),
    ("Turnover", "Urgent", "The resident moved in to find the HVAC filter missing, no water in the water heater, and the dishwasher still disconnected.",
     "Same-day dispatch resolved all items and the resident received a $150 move-in credit. Root cause was a skipped utility activation checklist, which has been added to the make-ready QA form."),
    ("Plumbing", "Emergency", "Sewage is backing up into the downstairs shower and tub, and the home has a strong odor.",
     "The main sewer line was cleared, and a camera inspection found a collapsed section of clay pipe. A line replacement was approved as a capital repair and the resident was moved to a hotel for 2 nights."),
    ("HVAC", "Routine", "The resident asked whether the air filter should be replaced, as none has been changed in 6 months.",
     "Filter delivery subscription was confirmed active but packages were going to the previous resident's address. The address was corrected and the filter was replaced during a courtesy visit."),
    ("Neighbor / HOA", "Routine", "The resident received an HOA notice that trash bins are visible from the street, which is not allowed in the community.",
     "Guidance on HOA rules was provided and the community welcome packet was updated for build-to-rent communities."),
    ("Electrical", "Urgent", "The ceiling fan in the primary bedroom wobbles badly and the light flickers.",
     "The fan mounting box was not fan-rated. A rated box was installed and the fan rebalanced."),
    ("Roofing", "Routine", "The resident noticed granules accumulating in the downspouts and a few curled shingles visible from the yard.",
     "The roof inspection estimated 3-5 years of remaining life. The property was added to the capital plan for roof replacement in 2027."),
    ("General Repair", "Routine", "The fence gate is broken and the resident's dog escaped twice this week.",
     "Gate hinges and latch were replaced. Fence condition was noted as fair, with a replacement estimate filed."),
    ("Pest Control", "Urgent", "The resident hears scratching in the attic at night and found droppings in the garage.",
     "A wildlife vendor identified roof rats and sealed entry points at soffits and roof vents. Traps were set and the property was scheduled for a 2-week follow-up."),
    ("Lease / Renewal", "Urgent", "The resident's renewal deadline is in 5 days and they have not received a renewal offer through the portal.",
     "An automated renewal workflow failure was found for 12 leases in the Phoenix market. Offers were generated manually and the integration error was logged for the systems team."),
    ("Billing / Account", "Routine", "The resident asked why their move-out security deposit disposition deducted $640 for paint when they lived in the home for 4 years.",
     "The deduction was reviewed against the normal wear-and-tear policy. Paint after 4 years of occupancy is normal wear, so $640 was refunded."),
    ("Water Mitigation", "Urgent", "The resident found the carpet wet along the wall shared by the water heater closet.",
     "The water heater tank had begun leaking at 13 years old and was replaced. A drain pan and leak sensor were installed and the carpet pad was replaced."),
    ("Doors & Windows", "Urgent", "A window in the child's bedroom will not latch after a storm and the screen is torn.",
     "The window sash was realigned, the latch replaced, and the screen rescreened. A window-safety check was completed."),
    ("Mold / Moisture", "Routine", "The resident noticed condensation dripping from the air vents and a damp smell in the hallway.",
     "Vent boots were insulated in the attic and the HVAC drain line was cleared. Humidity readings returned to normal on follow-up."),
]
tickets = []
for i, (cat, pri, desc, res) in enumerate(TICKETS, 1):
    pid = random.choice(properties)[0]
    tickets.append((f"T{i:04d}", pid, rand_date(date(2025, 6, 1), date(2026, 10, 15)).isoformat(),
                    cat, pri, random.choice(["Portal", "Portal", "Phone", "Email", "Text"]), desc, res))
write("resident_service_tickets", ["TICKET_ID", "PROPERTY_ID", "TICKET_DATE", "CATEGORY", "PRIORITY",
                                   "CHANNEL", "DESCRIPTION", "RESOLUTION_NOTES"], tickets)

# --- PROPERTY_INSPECTIONS (unstructured) ---------------------------------
INSPECTIONS = [
    ("Move-Out", 3, "Moderate wear consistent with a 3-year tenancy. Carpet in two bedrooms is stained beyond cleaning, interior walls need full repaint, and the kitchen faucet has a slow drip. HVAC filter was heavily loaded and the coil should be cleaned.", 4200),
    ("Move-Out", 2, "Significant damage beyond normal wear. Pet damage to flooring throughout the living area and doors, a broken window in the rear bedroom, and missing smoke detectors. The resident's security deposit will not cover estimated costs.", 9800),
    ("Move-Out", 4, "Home left in very good condition. Light touch-up paint, carpet cleaning, and replacement of two burned-out bulbs are the only items. Eligible for a fast-track 5-day make-ready.", 1100),
    ("Move-Out", 3, "Backyard fence has two missing panels and the irrigation controller is not functional. Interior is in fair condition, with laminate flooring lifting near the dishwasher from a possible slow leak that needs plumbing review.", 5300),
    ("Move-Out", 3, "Appliances are functional but dated; the range is 14 years old. Cabinet doors are loose and the hall bath vanity top is cracked. Recommend a value-add finish upgrade during the turn given the strong submarket rents.", 6700),
    ("Annual", 4, "Exterior and systems in good condition. Smoke and CO detectors tested and passed. The resident has added a raised garden bed, which is permitted. No action items.", 0),
    ("Annual", 3, "Water heater is 12 years old with minor corrosion at the inlet. Recommend proactive replacement within 6 months. Gutters are full of debris and the downspout extension is missing, causing ponding near the foundation.", 1850),
    ("Annual", 2, "Unauthorized pet (large dog) observed, plus extensive scratching on interior doors. Bathroom exhaust fan is not working and there is visible mildew. Lease compliance notice recommended, along with a moisture repair work order.", 1400),
    ("Annual", 4, "Home well maintained. The resident reported no issues. HVAC was serviced 3 months ago per the preventive maintenance schedule. Roof estimated at 8+ years of remaining life.", 0),
    ("Annual", 3, "Several outlets lack GFCI protection in wet areas. Attic insulation is compressed and below R-30. Recommend an energy efficiency upgrade bundle to reduce resident utility costs and HVAC run time.", 2900),
    ("Pre-Acquisition", 3, "Built 2003, original roof (~22 years) near end of life. HVAC replaced 2017. Foundation shows minor settlement cracks, typical for the region, with no structural concern noted. Underwriting should include roof replacement in the year-one capex budget.", 14500),
    ("Pre-Acquisition", 4, "Built 2016 in a strong school district. All major systems are under 10 years old. Minor cosmetic items only. Expected stabilized rent supports underwriting at the target yield.", 2200),
    ("Pre-Acquisition", 2, "Evidence of a prior roof leak with a stained ceiling and soft decking in one area. Polybutylene supply lines identified and must be repiped. Recommend a price reduction or pass, given about $28K in immediate capex.", 28000),
    ("Pre-Acquisition", 3, "The HOA has rental restrictions requiring a 12-month minimum lease and a cap of 20% rentals in the community, now at 17%. Property condition is fair. Confirm HOA rental eligibility before closing.", 6000),
    ("Make-Ready QA", 4, "All checklist items complete. Paint, flooring, and fixtures verified. Utilities active, smart lock provisioned, HVAC filter installed, and photos uploaded. Approved for listing.", 0),
    ("Make-Ready QA", 2, "Failed QA. Carpet not replaced in the primary bedroom as scoped, nail holes visible in the living room, and the pre-move-in pest treatment was not documented. Returned to the vendor with a 48-hour deadline.", 0),
    ("Make-Ready QA", 3, "Passed with exceptions. The dishwasher is not connected because of a back-ordered part and the ETA is 4 days. Listing approved with move-in date no earlier than the part installation.", 0),
    ("Annual", 3, "Exterior paint is peeling on the south-facing elevation and trim boards show wood rot near the garage. Recommend an exterior repaint in the next capital cycle, about $5,500.", 5500),
    ("Move-Out", 3, "Odor of smoke throughout the home despite the non-smoking lease. Requires an ozone treatment, sealing primer on all walls, and HVAC duct cleaning. Charge back to the resident per the lease addendum.", 3600),
    ("Storm Damage", 2, "Following the hurricane, a section of soffit and fascia was torn off, the fence is down on two sides, and water intruded at the rear sliding door. The home is habitable, and mitigation equipment is in place.", 11200),
    ("Storm Damage", 3, "Hail damage on the roof (12 hits per test square) and dented gutters. No interior intrusion. Insurance adjuster inspection is scheduled, and the roof is likely to be a full replacement under the claim.", 16000),
    ("Annual", 4, "Build-to-rent community home, 2 years old, under builder warranty. Resident reports a minor drywall crack above a doorway; logged as a warranty claim. No other issues.", 0),
    ("Annual", 2, "The pool fence gate does not self-close and latch, a safety and code violation. The pool pump motor is failing. Immediate safety work order issued.", 2400),
    ("Pre-Acquisition", 4, "Built 2019, includes a solar lease that would transfer to the owner. Review the solar lease terms. Systems are in excellent condition. Recommend acquisition at the asking price.", 1500),
    ("Make-Ready QA", 3, "Passed. Landscaping is below curb-appeal standard; the front beds need fresh mulch and two dead shrubs replaced before listing photos.", 450),
]
inspections = []
for i, (itype, rating, findings, est) in enumerate(INSPECTIONS, 1):
    inspections.append((f"INS{i:04d}", random.choice(properties)[0],
                        rand_date(date(2025, 3, 1), date(2026, 10, 10)).isoformat(),
                        itype, rating, findings, est,
                        random.choice(["R. Alvarez", "K. Patel", "D. Thompson", "M. Okafor", "S. Nguyen"])))
write("property_inspections", ["INSPECTION_ID", "PROPERTY_ID", "INSPECTION_DATE", "INSPECTION_TYPE",
                               "CONDITION_RATING", "FINDINGS", "ESTIMATED_REPAIR_COST", "INSPECTOR"], inspections)

# --- OPERATING_PROCEDURES (unstructured SOPs) ----------------------------
SOPS = [
    ("SOP-001", "Emergency Work Order Response Standard", "Maintenance",
     "Emergencies include no heat below 40 degrees outdoor temperature, no cooling above 85 degrees indoor temperature, active water intrusion, sewage backup, gas odor, electrical burning smell, and any condition that prevents securing the home. A vendor must acknowledge an emergency within 1 hour and be on site within 4 hours. If no vendor accepts in 30 minutes, the work order escalates automatically to the market maintenance manager. Residents with medically vulnerable household members get priority dispatch."),
    ("SOP-002", "Make-Ready Turnover Checklist", "Turnover",
     "Every vacated home must complete the make-ready checklist before listing. Required steps: move-out inspection with photos, scope approval within 48 hours, pre-move-in pest treatment, HVAC filter replacement and system test, water heater flush, smoke and CO detector test, smart lock reset, utility activation, and a QA inspection with photo upload. The target turn time is 10 days for standard scopes and 21 days for value-add scopes. A failed QA returns the home to the vendor at no additional cost."),
    ("SOP-003", "Renewal Pricing and Retention Guidelines", "Revenue Management",
     "Renewal offers are generated 75 days before lease expiration using the revenue management model. The model considers comparable market rents, home-level attributes, the resident's tenure and payment history, and portfolio occupancy targets. Community managers may approve retention concessions of up to 2 percentage points below the model offer for residents in good standing. Concessions beyond that require regional director approval. Renewal increases are capped where local regulation requires."),
    ("SOP-004", "Security Deposit Disposition Policy", "Leasing",
     "Deposit dispositions must be issued within the state-mandated timeline, typically 14 to 45 days depending on the state. Deductions require move-out photo evidence and must exclude normal wear and tear. Paint is considered normal wear after 3 or more years of occupancy, and carpet after 5 or more years. Itemized statements must include vendor invoices for any deduction over $250."),
    ("SOP-005", "Moisture and Mold Response Procedure", "Health & Safety",
     "Any report of visible mold, persistent moisture, or a musty odor requires an inspection within 72 hours, or within 24 hours if a household member has a respiratory condition. The inspector identifies the moisture source first, since remediation without source correction is not allowed. Areas over 10 square feet require a licensed remediation vendor. Temporary lodging is offered when remediation affects bedrooms or when medically advised."),
    ("SOP-006", "Vendor Performance Scorecard", "Vendor Management",
     "Vendors are scored monthly on SLA compliance, first-time fix rate, QA pass rate, cost versus benchmark, and resident satisfaction. A score under 70 for two consecutive months triggers a performance improvement plan. Preferred vendor status requires a score of 85 or higher, current insurance certificates, and background-checked technicians. Missed scheduled services such as landscaping are logged as scorecard deductions."),
    ("SOP-007", "Preventive Maintenance Program", "Maintenance",
     "Each home receives semi-annual HVAC service, before cooling and heating seasons. Filters ship to residents every 60 days. Water heaters older than 10 years are inspected annually and proactively replaced at 12 years or at the first sign of corrosion. Roofs are visually inspected annually. Gutters are cleaned annually, or twice a year in heavily wooded lots."),
    ("SOP-008", "Capital Expenditure Approval Thresholds", "Asset Management",
     "Repairs under $2,500 may be approved by the market maintenance manager. Repairs from $2,500 to $10,000 require regional director approval. Repairs over $10,000, roof replacements, sewer line replacements, and HVAC system replacements require asset management approval with a repair-versus-dispose analysis. Insurance claims should be opened for any storm, hail, or water event where damage may exceed the deductible."),
    ("SOP-009", "Early Lease Termination and Transfer Policy", "Leasing",
     "Residents may terminate early with 60 days' notice and a fee equal to one month's rent. Residents relocating between markets in the portfolio may transfer with no termination fee, subject to approval of the new home. Military residents receive protections under the Servicemembers Civil Relief Act. Domestic violence early termination is handled confidentially according to state law."),
    ("SOP-010", "Storm and Hurricane Preparedness", "Health & Safety",
     "Florida, Texas, and Carolinas markets activate the storm plan 72 hours before projected landfall. Residents receive preparation notices, and vendors are pre-staged for tarping, debris removal, and water mitigation. After the storm, every home in the affected area is surveyed within 5 days, prioritizing homes reporting intrusion or loss of utilities. All damage is photographed for insurance claims."),
    ("SOP-011", "Resident Communication Standards", "Resident Experience",
     "Resident inquiries via portal, text, or email receive a first response within 4 business hours. Every work order sends status updates at scheduling, dispatch, and completion. Satisfaction surveys are sent within 24 hours of completion. Any rating of 1 or 2 triggers a callback from the community manager within 2 business days."),
    ("SOP-012", "Pest Control Standards", "Maintenance",
     "Every turnover requires an interior and exterior pest treatment before move-in, documented in the make-ready record. Resident-reported pest issues within 30 days of move-in are treated at no charge. Florida and Texas homes receive quarterly exterior treatments. Rodent issues require exclusion work, sealing entry points, and not just trapping."),
    ("SOP-013", "Smart Home Device Management", "Technology",
     "All homes have a smart lock, smart thermostat, and leak sensors under sinks and water heaters. Access codes are rotated at every turnover and vendor codes expire within 24 hours of the scheduled visit. Leak-sensor alerts create an urgent work order automatically. Residents may not remove smart devices, but they may connect them to their own accounts."),
    ("SOP-014", "Delinquency and Payment Plan Procedure", "Revenue Management",
     "Rent is due on the 1st, and a late fee applies after the 5th unless prohibited locally. Residents experiencing hardship may request a payment plan of up to 3 months. Before filing any eviction, the team must attempt resident outreach on three separate days and refer the resident to rental assistance resources. Bulk fee waivers are issued for payment processor outages."),
    ("SOP-015", "Value-Add Renovation Scope Standards", "Asset Management",
     "During turnover, homes in submarkets where rents support a premium of 8% or more are evaluated for value-add upgrades: luxury vinyl plank flooring, quartz countertops, LED lighting, updated fixtures, and smart home packages. Upgrade budgets are capped at $12,000 per home unless approved by asset management. The renovation ROI must exceed 10% based on incremental rent."),
    ("SOP-016", "Build-to-Rent Community Operations", "Operations",
     "Build-to-rent communities have on-site amenity management, HOA-style rules communicated at lease signing, and builder warranty tracking for the first 24 months. Warranty items must be filed with the builder before using portfolio vendors. Common-area landscaping and amenities follow the community operations calendar."),
    ("SOP-017", "Water Heater Replacement Standard", "Maintenance",
     "Replacement water heaters must be at least 50 gallons for homes with four or more bedrooms. They require a drain pan, a leak sensor, and a code-compliant expansion tank. Gas units need a combustion air check. Replacements are scheduled within 24 hours for no-hot-water emergencies."),
    ("SOP-018", "HOA Compliance Management", "Operations",
     "HOA violation notices must be logged within 1 business day and resolved before the cure deadline. Violations caused by vendor service failures are charged back to the vendor. Violations caused by residents are communicated with the HOA rule excerpt and a cure timeline. Repeat resident violations may result in a lease compliance notice."),
    ("SOP-019", "Resident Move-In Experience", "Resident Experience",
     "Move-in day requires utilities active, a smart lock code delivered, a welcome packet with HOA rules and the maintenance request guide, a move-in condition report available in the portal for 7 days, and a filter delivery subscription activated. A 7-day post-move-in check-in call is required. Move-in defects found within 7 days are prioritized as urgent."),
    ("SOP-020", "Data Definitions for Operating KPIs", "Analytics",
     "Occupancy = occupied homes divided by total homes in the operating portfolio, excluding homes under renovation over 30 days and homes held for sale. Blended rent growth = weighted average of renewal and new lease rent change. Days to re-lease = days from move-out to the next lease start. Turnover rate = annualized move-outs divided by average occupied homes. Bad debt = uncollectible rent as a percentage of billed rent. These definitions should match Power BI reporting."),
]
sops = [(s[0], s[1], s[2], rand_date(date(2024, 1, 1), date(2026, 6, 30)).isoformat(), s[3]) for s in SOPS]
write("operating_procedures", ["DOC_ID", "TITLE", "CATEGORY", "EFFECTIVE_DATE", "CONTENT"], sops)
