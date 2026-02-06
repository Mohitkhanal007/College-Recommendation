import json
import random

# Real colleges found from verified sources
real_colleges = [
    # Engineering
    {"name": "Pulchowk Campus (IOE)", "location": "Lalitpur", "type": "Government", "programs": ["Aerospace Engineering", "Chemical Engineering", "Computer Engineering", "Civil Engineering", "Mechanical Engineering", "Electrical Engineering"]},
    {"name": "Thapathali Campus (IOE)", "location": "Kathmandu", "type": "Government", "programs": ["Industrial Engineering", "Automobile Engineering", "Computer Engineering", "Civil Engineering", "Mechanical Engineering"]},
    {"name": "National College of Engineering (NCE)", "location": "Lalitpur", "type": "Private", "programs": ["Civil Engineering", "Computer Engineering", "Electronics Engineering", "Electrical Engineering"]},
    {"name": "Nepal College of Information Technology (NCIT)", "location": "Lalitpur", "type": "Private", "programs": ["Software Engineering", "IT Engineering", "Computer Engineering", "Civil Engineering", "BBA", "BCA"]},
    {"name": "Khwopa Engineering College", "location": "Bhaktapur", "type": "Community", "programs": ["Architecture", "Civil Engineering", "Computer Engineering", "Electrical Engineering"]},
    {"name": "Himalaya College of Engineering", "location": "Lalitpur", "type": "Private", "programs": ["Computer Engineering", "Electronics Engineering", "Civil Engineering"]},
    {"name": "Kantipur Engineering College", "location": "Lalitpur", "type": "Private", "programs": ["Civil Engineering", "Computer Engineering", "Electronics Engineering"]},
    {"name": "Kathmandu Engineering College", "location": "Kathmandu", "type": "Private", "programs": ["Architecture", "Civil Engineering", "Computer Engineering", "Electronics Engineering", "Electrical Engineering"]},
    {"name": "Janakpur Engineering College", "location": "Lalitpur", "type": "Private", "programs": ["Civil Engineering", "Computer Engineering", "Electronics Engineering"]},
    {"name": "Gandaki College of Engineering and Science", "location": "Pokhara", "type": "Private", "programs": ["Software Engineering", "Computer Engineering", "Information Technology"]},
    {"name": "Nepal Engineering College", "location": "Bhaktapur", "type": "Private", "programs": ["Architecture", "Civil Engineering", "Computer Engineering", "Electronics Engineering", "Electrical Engineering", "Civil and Rural Engineering"]},
    {"name": "Pashchimanchal Campus (IOE)", "location": "Pokhara", "type": "Government", "programs": ["Civil Engineering", "Computer Engineering", "Electronics Engineering", "Electrical Engineering", "Geomatics Engineering", "Mechanical Engineering"]},
    {"name": "Purwanchal Campus (IOE)", "location": "Dharan", "type": "Government", "programs": ["Agricultural Engineering", "Civil Engineering", "Computer Engineering", "Electronics Engineering", "Mechanical Engineering"]},
    {"name": "Lalitpur Engineering College", "location": "Lalitpur", "type": "Private", "programs": ["Civil Engineering", "Computer Engineering"]},
    {"name": "Madan Bhandari Memorial Academy Nepal", "location": "Morang", "type": "Community", "programs": ["Computer Engineering", "Civil Engineering"]},
    {"name": "Sagarmatha Engineering College", "location": "Lalitpur", "type": "Private", "programs": ["Civil Engineering", "Computer Engineering", "Electronics Engineering"]},
    {"name": "Cosmos College of Management and Technology", "location": "Lalitpur", "type": "Private", "programs": ["BBA", "Civil Engineering", "Computer Engineering", "Electronics Engineering", "IT"]},
    {"name": "Ritz College of Engineering and Management", "location": "Lalitpur", "type": "Private", "programs": ["Civil Engineering", "Hotel Management", "BBA"]},
    
    # Management & General
    {"name": "Kathmandu Model College (KMC)", "location": "Kathmandu", "type": "Private", "programs": ["BBA", "BBS", "BCA", "BA Social Work", "MA English"]},
    {"name": "DAV College", "location": "Lalitpur", "type": "Private", "programs": ["BBA", "BBS", "BBM", "BSc Physics", "BSc Microbiology"]},
    {"name": "Padmashree College", "location": "Kathmandu", "type": "Private", "programs": ["BBA", "BHM", "BIT", "BTech Food"]},
    {"name": "Campion College", "location": "Lalitpur", "type": "Private", "programs": ["BBA", "BBS", "BA", "BA Social Work"]},
    {"name": "Thames College", "location": "Kathmandu", "type": "Private", "programs": ["BBA", "BIM", "BCA", "BA Social Work", "BBM"]},
    {"name": "Kathford International College", "location": "Lalitpur", "type": "Private", "programs": ["BBA", "BBM", "Computer Engineering", "Civil Engineering"]},
    {"name": "Kantipur College of Management and IT", "location": "Kathmandu", "type": "Private", "programs": ["BBA", "BIM"]},
    {"name": "Ace Institute of Management", "location": "Kathmandu", "type": "Private", "programs": ["BBA", "MBA", "BBA-BI"]},
    {"name": "Uniglobe College", "location": "Kathmandu", "type": "Private", "programs": ["BBA", "MBA", "BBA-BI"]},
    {"name": "Quest International College", "location": "Lalitpur", "type": "Private", "programs": ["BBA", "BHM", "MBA"]},
    {"name": "Liberty College", "location": "Kathmandu", "type": "Private", "programs": ["BBA"]},
    {"name": "South Asian Institute of Management (SAIM)", "location": "Kathmandu", "type": "Private", "programs": ["BBA", "MBA"]},
    {"name": "Kantipur Valley College", "location": "Lalitpur", "type": "Private", "programs": ["BBA", "MBA", "BTech", "EMBA"]},
    {"name": "Himalayan Whitehouse International College", "location": "Kathmandu", "type": "Private", "programs": ["BBA", "BTech", "Liberal Arts", "BE Civil"]},
    {"name": "Shankar Dev Campus", "location": "Kathmandu", "type": "Government", "programs": ["BBS", "BBA", "BIM", "BBM", "MBS"]},
    {"name": "Nepal Commerce Campus", "location": "Kathmandu", "type": "Government", "programs": ["BBS", "BBA", "BBM", "BIM", "MBS"]},
    {"name": "Padma Kanya Multiple Campus", "location": "Kathmandu", "type": "Government", "programs": ["BBA", "BBS", "BCA", "BA", "BIT", "MA"]},
    # Pokhara
    {"name": "Gandaki College of Engineering and Science", "location": "Pokhara", "type": "Private", "programs": ["Software Engineering", "Computer Engineering", "Information Technology", "BSc CSIT"]},
    {"name": "Pokhara Engineering College", "location": "Pokhara", "type": "Private", "programs": ["Civil Engineering", "Computer Engineering", "Electronics Engineering", "Architecture"]},
    {"name": "Prithvi Narayan Campus", "location": "Pokhara", "type": "Government", "programs": ["BSc CSIT", "BSc Physics", "BSc Chemistry", "BBS", "BA", "BEd", "LLB", "MSc", "BPA"]},
    {"name": "LA Grandee International College", "location": "Pokhara", "type": "Private", "programs": ["BCA", "BBA", "BPH"]},
    {"name": "Informatics College Pokhara", "location": "Pokhara", "type": "Private", "programs": ["BSc IT", "BBA"]},
    {"name": "Pokhara College of Management", "location": "Pokhara", "type": "Private", "programs": ["BBA", "BCIS"]},
    {"name": "Janapriya Multiple Campus", "location": "Pokhara", "type": "Community", "programs": ["BSc Microbiology", "BSc Environmental Science", "BBA", "BBS", "MBS"]},
    {"name": "Mount Annapurna Campus", "location": "Pokhara", "type": "Private", "programs": ["BSc CSIT", "BSc"]},
    {"name": "Soch College of IT", "location": "Pokhara", "type": "Private", "programs": ["BSc CSIT", "BCA"]},

    # Biratnagar
    {"name": "Mahendra Morang Adarsha Multiple Campus", "location": "Biratnagar", "type": "Government", "programs": ["BSc", "BBS", "BA", "BEd", "BPA", "BIT", "BSc CSIT"]},
    {"name": "Purbanchal University School of Management (PUSOM)", "location": "Biratnagar", "type": "Government", "programs": ["BBA", "MBA"]},
    {"name": "Eastern College of Engineering", "location": "Biratnagar", "type": "Private", "programs": ["Computer Engineering", "Civil Engineering", "Electronics Engineering"]},
    {"name": "Birat Multiple College", "location": "Biratnagar", "type": "Private", "programs": ["BSc CSIT", "BCA"]},
    {"name": "AIMS College", "location": "Biratnagar", "type": "Private", "programs": ["BSc CSIT", "BCA", "BBS"]},
    {"name": "Nihareeka College", "location": "Biratnagar", "type": "Private", "programs": ["BSc CSIT", "BCA", "BBS", "BIM"]},
    {"name": "Birat Kshitiz College", "location": "Biratnagar", "type": "Private", "programs": ["BSc CSIT", "BCA", "BBM"]},
    {"name": "Purbanchal University School of Engineering", "location": "Biratnagar", "type": "Government", "programs": ["Software Engineering", "Computer Engineering", "Civil Engineering"]},

    # Chitwan / Bharatpur
    {"name": "Birendra Multiple Campus", "location": "Chitwan", "type": "Government", "programs": ["BSc", "BBS", "BA", "BEd", "MSc Physics", "CSIT", "BSc CSIT"]},
    {"name": "Valley State College", "location": "Chitwan", "type": "Private", "programs": ["BBA", "BSc Nursing", "BPH"]},
    {"name": "United Technical College (U-TEC)", "location": "Chitwan", "type": "Private", "programs": ["Civil Engineering", "Computer Engineering", "Electrical Engineering"]},
    {"name": "Nepal Polytechnic Institute", "location": "Chitwan", "type": "Private", "programs": ["Civil Engineering", "Electrical Engineering", "BSc Agriculture"]},
    {"name": "Chitwan Engineering Campus", "location": "Chitwan", "type": "Government", "programs": ["Architecture", "Civil Engineering"]},
    {"name": "Boston International College", "location": "Chitwan", "type": "Private", "programs": ["BBA", "BBA-BI", "BCIS"]},
    {"name": "Indreni College", "location": "Chitwan", "type": "Private", "programs": ["BSc CSIT", "BCA"]},

    # Butwal / Rupandehi
    {"name": "Butwal Model College", "location": "Butwal", "type": "Private", "programs": ["BBA", "BBA-BI"]},
    {"name": "Lumbini Banijya Campus", "location": "Butwal", "type": "Community", "programs": ["BBS", "BBM", "BBA", "MBA-BF"]},
    {"name": "Crimson College of Technology", "location": "Butwal", "type": "Private", "programs": ["BBA", "BCA", "BCIS", "B Pharmacy"]},
    {"name": "Butwal Multiple Campus", "location": "Butwal", "type": "Government", "programs": ["BSc CSIT", "BEd", "BBS", "BA", "BICTE"]},
    {"name": "Siddhartha International College", "location": "Butwal", "type": "Private", "programs": ["BBA", "BBA-BI"]},
    {"name": "Nepathya College", "location": "Butwal", "type": "Private", "programs": ["BSc CSIT", "BCA"]},
    {"name": "Tilottama Campus", "location": "Butwal", "type": "Private", "programs": ["BBA", "BSc", "BBS"]},

    # Dharan / Itahari
    {"name": "Purwanchal Campus (IOE)", "location": "Dharan", "type": "Government", "programs": ["Agricultural Engineering", "Civil Engineering", "Computer Engineering", "Electronics Engineering", "Mechanical Engineering"]},
    {"name": "B.P. Koirala Institute of Health Sciences", "location": "Dharan", "type": "Government", "programs": ["MBBS", "BSc Nursing", "BDS", "BPH"]},
    {"name": "Sunsari Multiple Campus", "location": "Dharan", "type": "Community", "programs": ["BSc", "BBS", "BA", "BEd"]},
    {"name": "Itahari Namuna College", "location": "Itahari", "type": "Private", "programs": ["BCA", "BBS", "BA", "BSW", "BHM"]},
    {"name": "Kasturi College", "location": "Itahari", "type": "Private", "programs": ["BBA", "BBS"]},
    {"name": "Sushma Godawari College", "location": "Itahari", "type": "Private", "programs": ["BSc CSIT", "BBS", "BBA", "BCA"]},
    {"name": "Dharan College of Management", "location": "Dharan", "type": "Private", "programs": ["BBA", "MBA"]},

    # Nepalgunj / Dhangadhi
    {"name": "Nepalgunj Medical College", "location": "Nepalgunj", "type": "Private", "programs": ["MBBS", "BSc Nursing"]},
    {"name": "Nepalgunj College", "location": "Nepalgunj", "type": "Private", "programs": ["BSc CSIT", "BCA", "BBS"]},
    {"name": "Brightland College", "location": "Nepalgunj", "type": "Private", "programs": ["BIM", "BBS"]},
    {"name": "Kailali Multiple Campus", "location": "Dhangadhi", "type": "Community", "programs": ["BBS", "BA", "BEd", "BSc"]},
    {"name": "Asian Byabasthapan College", "location": "Dhangadhi", "type": "Private", "programs": ["BBS", "BHCM", "BIM"]},
    {"name": "Sudur Paschimanchal Campus", "location": "Dhangadhi", "type": "Private", "programs": ["BBA", "BEd", "BSc"]},
    
    # Other Locations
    {"name": "Hetauda School of Management", "location": "Hetauda", "type": "Private", "programs": ["BIM", "BBA", "BBS"]},
    {"name": "Janapriya Multiple Campus", "location": "Hetauda", "type": "Community", "programs": ["BBS", "BEd", "BA"]},
    {"name": "Makwanpur Multiple Campus", "location": "Hetauda", "type": "Community", "programs": ["BBS", "BA", "BEd"]},
    
    # IT & Computing (Specific Requests)
    {"name": "Herald College", "location": "Kathmandu", "type": "Private", "programs": ["BIT", "BSc Computer Science", "International Business"]},
    {"name": "The British College", "location": "Kathmandu", "type": "Private", "programs": ["BBA", "BHM", "BSc Computing", "BIT", "MBA"]},
    {"name": "Islington College", "location": "Kathmandu", "type": "Private", "programs": ["BSc Computing", "BSc Networking", "BIT", "BBA", "BHM"]},
    {"name": "Softwarica College of IT and E-Commerce", "location": "Kathmandu", "type": "Private", "programs": ["BSc Computing", "BIT", "Ethical Hacking"]},
    {"name": "International School of Management and Technology (ISMT)", "location": "Kathmandu", "type": "Private", "programs": ["BBA", "BHM", "BIT"]},
    {"name": "Deerwalk Institute of Technology", "location": "Kathmandu", "type": "Private", "programs": ["BSc CSIT", "BCA"]},
    {"name": "Texas International College", "location": "Kathmandu", "type": "Private", "programs": ["BSc CSIT", "BCA", "BBS", "BBA"]},
    {"name": "Orchid International College", "location": "Kathmandu", "type": "Private", "programs": ["BSc CSIT", "BIM", "BCA", "BBM", "BSW"]},
    {"name": "Samriddhi College", "location": "Bhaktapur", "type": "Private", "programs": ["BSc CSIT", "BCA", "BBS", "BA Social Work"]},
    {"name": "Nagarjuna College of Information Technology", "location": "Lalitpur", "type": "Private", "programs": ["BSc CSIT", "BCA", "BIM"]},
    {"name": "Swastik College", "location": "Bhaktapur", "type": "Private", "programs": ["BSc CSIT", "BCA"]},
    {"name": "Amrit Science Campus", "location": "Kathmandu", "type": "Government", "programs": ["BSc CSIT", "BSc Physics", "BSc Chemistry", "BSc Microbiology", "BSc Botany", "BSc Zoology"]},
    {"name": "Patan Multiple Campus", "location": "Lalitpur", "type": "Government", "programs": ["BSc CSIT", "BCA", "BBS", "BA", "BSc"]},
    {"name": "St. Xavier's College", "location": "Kathmandu", "type": "Private", "programs": ["BSc CSIT", "BSc Physics", "BSc Microbiology", "BA Social Work", "BBS"]},

    # Medical & Nursing
    {"name": "Kathmandu University School of Medical Sciences", "location": "Dhulikhel", "type": "Private", "programs": ["MBBS", "BSc Nursing", "BDS", "BPT"]},
    {"name": "Chitwan Medical College", "location": "Chitwan", "type": "Private", "programs": ["MBBS", "BSc Nursing", "BDS", "BPH"]},
    {"name": "College of Medical Science", "location": "Chitwan", "type": "Private", "programs": ["MBBS", "BSc Nursing", "BDS"]},
    {"name": "Nepalgunj Medical College", "location": "Nepalgunj", "type": "Private", "programs": ["MBBS", "BSc Nursing"]},
    {"name": "Universal College of Medical Sciences", "location": "Bhairahawa", "type": "Private", "programs": ["MBBS", "BSc Nursing", "BDS"]},
    {"name": "Kathmandu Medical College", "location": "Kathmandu", "type": "Private", "programs": ["MBBS", "BSc Nursing", "BDS"]},
    {"name": "Lumbini Medical College", "location": "Palpa", "type": "Private", "programs": ["MBBS", "BSc Nursing"]},
    {"name": "Pokhara Nursing Campus", "location": "Pokhara", "type": "Government", "programs": ["BSc Nursing", "BNS"]},
    {"name": "Maharajgunj Medical Campus", "location": "Kathmandu", "type": "Government", "programs": ["MBBS", "BSc Nursing", "BPH", "BMLT", "B.Optom"]},
    {"name": "B.P. Koirala Institute of Health Sciences", "location": "Dharan", "type": "Government", "programs": ["MBBS", "BSc Nursing", "BDS", "BPH"]},
    {"name": "Manipal College of Medical Sciences", "location": "Pokhara", "type": "Private", "programs": ["MBBS", "BSc Nursing", "BDS"]},
    {"name": "Nobel Medical College", "location": "Biratnagar", "type": "Private", "programs": ["MBBS", "BDS", "BSc Nursing"]},
    {"name": "Kist Medical College", "location": "Lalitpur", "type": "Private", "programs": ["MBBS", "BDS"]},
    {"name": "Birat Medical College", "location": "Biratnagar", "type": "Private", "programs": ["MBBS", "BSc Nursing"]},
    
    # Humanities & Others
    {"name": "Tri-Chandra Multiple Campus", "location": "Kathmandu", "type": "Government", "programs": ["BSc Physics", "BSc Chemistry", "BSc Geology","BA Psychology", "BA Social Work"]},
    {"name": "Ratna Rajya Laxmi Campus", "location": "Kathmandu", "type": "Government", "programs": ["BA English", "BA Journalism", "BA Economics", "BA Political Science"]},
    {"name": "Bhaktapur Multiple Campus", "location": "Bhaktapur", "type": "Government", "programs": ["BBS", "BA", "BSc"]},
    {"name": "Aberdeen International College", "location": "Lalitpur", "type": "Private", "programs": ["BBA", "BHM"]},
    {"name": "GoldenGate International College", "location": "Kathmandu", "type": "Private", "programs": ["BSc", "BBA", "BBS", "BA", "BSW"]}
]

program_types = {
    "Engineering": ["Civil Engineering", "Computer Engineering", "Software Engineering", "IT Engineering", "Electronics Engineering", "Electrical Engineering", "Mechanical Engineering", "Architecture", "Geomatics Engineering", "Biomedical Engineering"],
    "Management": ["BBA", "BBS", "BIM", "BHM", "BTTM", "BBM", "BPA", "BBA-BI", "BBA-Finance", "MBA", "EMBA"],
    "IT": ["BSc CSIT", "BCA", "BIT", "BE Computer", "BE Software", "BE IT", "BSc Computing", "BSc Networking"],
    "Science": ["BSc Physics", "BSc Chemistry", "BSc Biology", "BSc Microbiology", "BSc Environmental Science", "BSc Statistics", "BSc Mathematics", "BSc Geology", "BSc"],
    "Medical": ["MBBS", "BDS", "BSc Nursing", "BPH", "B Pharmacy", "BMLT", "B.Optom", "BAMS", "BPT"],
    "Humanities": ["BA English", "BA Major English", "BA Economics", "BA Sociology", "BA Psychology", "BA Journalism", "BA Social Work", "BA Political Science", "BA Rural Development", "BA", "BSW", "BEd"],
    "Agriculture": ["BSc Agriculture", "BVSc & AH", "BSc Forestry", "BTech Food Technology", "BTech Food"]
}

streams_map = {
    "Engineering": "Science",
    "IT": "Science",
    "Science": "Science",
    "Medical": "Science",
    "Agriculture": "Science",
    "Management": "Management",
    "Humanities": "Humanities"
}

def main():
    colleges = []
    college_id = 1
    
    print(f"Generating dataset with {len(real_colleges)} REAL colleges only.")
    
    for rc in real_colleges:
        # Determine category for metadata
        category = "General"
        programs = rc["programs"]
        stream = "Science" # Default
        
        # Heuristic to find category and stream
        for cat, progs in program_types.items():
            if any(p in str(programs) for p in progs):
                category = cat
                stream = streams_map[cat]
                break
        
        # Ensure 'streams' is a list
        streams = [stream]
        if "Management" in str(programs) or "BBA" in str(programs) or "BBS" in str(programs):
            if "Management" not in streams: streams.append("Management")
        if "BA" in str(programs) or "BSW" in str(programs):
             if "Humanities" not in streams: streams.append("Humanities")
        
        budget = random.choice(["low", "medium", "high"])
        if rc.get("type") == "Government" or rc.get("type") == "Community":
            budget = "low"
        elif "International" in rc["name"] or "British" in rc["name"] or "Islington" in rc["name"]:
            budget = "high"
            
        colleges.append({
            "id": college_id,
            "name": rc["name"],
            "location": rc["location"],
            "programs": programs,
            "streams": streams,
            "min_gpa": round(random.uniform(2.4, 3.2), 1) if rc.get("type") == "Government" else round(random.uniform(2.0, 3.0), 1),
            "budget_range": budget,
            "career_focus": [category, "Industry"], 
            "interests": [category, "Learning"], 
            "description": f"{rc['name']} is a well-known {rc.get('type')} institution located in {rc['location']}.", 
            "website": f"https://example.com/college{college_id}",
            "contact": f"+977-1-{random.randint(4000000, 4999999)}",
            "facilities": ["Library", "Computer Lab", "Cafeteria", "WiFi"] + (["Hostel"] if random.random() > 0.4 else []),
            "established": random.randint(1960, 2010),
            "type": rc.get("type", "Private"),
            "admission_process": "Entrance Exam" if "Science" in streams else "Merit-based",
            "scholarship_available": True
        })
        college_id += 1
        
    # Save to file
    with open('data/colleges.json', 'w', encoding='utf-8') as f:
        json.dump(colleges, f, indent=2)
    
    print(f"Generated {len(colleges)} colleges.")

if __name__ == "__main__":
    main()
