from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
import datetime
import os 
import re
import openai
from excel_utils import append_to_excel

app = Flask(__name__)
app.config['SECRET_KEY'] = 'isro_kiosk_2025'

# OpenAI API configuration
OPENAI_API_KEY = "your-api-key-here"  # Replace with your API key
openai.api_key = OPENAI_API_KEY

# ISRO Knowledge Base with expanded topics
ISRO_KNOWLEDGE = {
    'isro': {
        'pattern': r'what.*(isro|indian space research)|about.*isro|tell.*isro',
        'response': '''ISRO (Indian Space Research Organisation) is India's national space agency, established in 1969. 
        It is one of the largest space agencies in the world and has achieved numerous milestones in space exploration. 
        ISRO's primary vision is to "harness space technology for national development while pursuing space science 
        research and planetary exploration".'''
    },
    'chandrayaan': {
        'pattern': r'chandrayaan|moon mission|lunar mission|lunar landing',
        'response': '''The Chandrayaan program represents India's lunar exploration missions:
        - Chandrayaan-1 (2008): First lunar mission that discovered water molecules on the Moon
        - Chandrayaan-2 (2019): Studied the Moon's surface with an orbiter (still operational)
        - Chandrayaan-3 (2023): Achieved historic soft landing on the Moon's south pole region, making India the fourth country to achieve a soft landing on the Moon and the first to land near the lunar south pole.'''
    },
    'mangalyaan': {
        'pattern': r'mangalyaan|mars mission|mars orbiter|mom',
        'response': '''Mangalyaan (Mars Orbiter Mission) was India's first interplanetary mission, launched in 2013. 
        It successfully reached Mars orbit in 2014, making ISRO the fourth space agency to reach Mars. 
        The mission demonstrated India's capability in deep space missions while being the most cost-effective Mars mission globally.'''
    },
    'gaganyaan': {
        'pattern': r'gaganyaan|human spaceflight|manned mission',
        'response': '''Gaganyaan is India's first human spaceflight program, aiming to demonstrate human spaceflight capability. 
        The mission will send astronauts to an orbit of 400km for 3 days. Key features include:
        - Indigenous development of human-rated launch vehicle
        - Life support systems and crew escape mechanisms
        - Extensive astronaut training program
        The first crewed mission is planned for 2025.'''
    },
    'aditya': {
        'pattern': r'aditya|solar mission|sun mission',
        'response': '''Aditya-L1 is India's first solar mission, designed to study the Sun from the Lagrangian point L1. 
        The mission carries various instruments to observe the solar corona, photosphere, and chromosphere. 
        It will help understand solar weather and its impact on Earth.'''
    },
    'pslv': {
        'pattern': r'pslv|polar satellite|launch vehicle',
        'response': '''The Polar Satellite Launch Vehicle (PSLV) is ISRO's reliable workhorse launch vehicle. 
        It has successfully conducted over 50 missions, launching various Indian and international satellites. 
        Known for its versatility and cost-effectiveness, PSLV has launched satellites to various orbits and even to the Moon and Mars.'''
    },
    'satellites': {
        'pattern': r'satellite program|communication satellite|earth observation',
        'response': '''ISRO's satellite program includes:
        - Communication satellites (INSAT/GSAT series)
        - Earth observation satellites (IRS series)
        - Navigation satellites (NavIC/IRNSS)
        - Scientific and planetary observation satellites
        These satellites support telecommunications, broadcasting, weather forecasting, and disaster management.'''
    },
    'achievements': {
        'pattern': r'achievement|success|milestone|recent.*development',
        'response': '''ISRO's notable achievements include:
        - Successful Chandrayaan-3 lunar landing (2023)
        - Mars Orbiter Mission success
        - Development of indigenous cryogenic engine
        - Launch of 104 satellites in a single mission
        - Demonstration of anti-satellite capabilities
        - Successful space capsule recovery experiment
        - Development of NavIC navigation system'''
    },
    'future': {
        'pattern': r'future|upcoming|plan|next mission',
        'response': '''ISRO's future plans include:
        - Gaganyaan human spaceflight mission
        - Shukrayaan Venus mission
        - Space station development
        - Reusable launch vehicle technology
        - Advanced satellite series
        - Deep space exploration missions
        These missions demonstrate ISRO's commitment to advancing India's space capabilities.'''
    },
    'budget': {
        'pattern': r'budget|cost|funding|financial',
        'response': '''ISRO is known for its cost-effective space missions:
        - Annual budget (2023-24): approximately ₹13,700 crore ($1.6 billion)
        - Chandrayaan-3 mission cost: ₹615 crore ($75 million)
        - Mars Orbiter Mission: ₹450 crore ($74 million)
        - Known for achieving complex missions at fraction of international costs
        ISRO's efficient resource utilization has made India a preferred partner for international space projects.'''
    },
    'technology': {
        'pattern': r'technology|innovation|development|indigenous',
        'response': '''Key technologies developed by ISRO:
        - Cryogenic Engine Technology
        - Reusable Launch Vehicle (RLV) Technology
        - Satellite Communication Systems
        - Remote Sensing Technologies
        - Navigation Systems (NavIC)
        - Space-Grade Lithium-Ion Cells
        These developments have made India self-reliant in space technology.'''
    },
    'international': {
        'pattern': r'international|collaboration|partnership|cooperation',
        'response': '''ISRO's International Collaborations:
        - Partnerships with NASA, ESA, JAXA, and other space agencies
        - Commercial launch services for multiple countries
        - Joint satellite missions
        - Technology exchange programs
        - International space research projects
        - Training programs for developing nations'''
    },
    'education': {
        'pattern': r'education|training|learn|study|course',
        'response': '''ISRO's Educational Initiatives:
        - Space Science Research Programs
        - ISRO Young Scientist Programme
        - Space Technology Cells in IITs
        - Training programs at Space Applications Centre
        - Collaborations with universities
        - Online courses and resources
        These programs aim to nurture future space scientists and engineers.'''
    },
    'applications': {
        'pattern': r'application|use|benefit|impact',
        'response': '''ISRO's Technology Applications:
        - Disaster Management
        - Weather Forecasting
        - Agriculture and Crop Monitoring
        - Urban Planning
        - Natural Resource Management
        - Telemedicine and Education
        - Navigation and Location Services
        These applications directly benefit society and economic development.'''
    },
    'history': {
        'pattern': r'history|establishment|origin|begin|start',
        'response': '''ISRO's Historical Journey:
        1962: Indian National Committee for Space Research established
        1969: ISRO formed
        1975: First Indian satellite Aryabhata launched
        1980: First indigenous satellite launch (Rohini)
        1984: First Indian astronaut in space (Rakesh Sharma)
        2008: First lunar mission
        2014: Successful Mars mission
        2023: Soft landing on Moon's south pole'''
    },
    'rockets': {
        'pattern': r'rocket|gslv|slv|launcher',
        'response': '''ISRO's Launch Vehicles:
        - SLV (Satellite Launch Vehicle)
        - ASLV (Augmented Satellite Launch Vehicle)
        - PSLV (Polar Satellite Launch Vehicle)
        - GSLV (Geosynchronous Satellite Launch Vehicle)
        - GSLV Mark III/LVM3 (Human-rated)
        Each vehicle serves specific mission requirements and payload capacities.'''
    },
    'shukrayaan': {
        'pattern': r'shukrayaan|venus mission|venus',
        'response': '''Shukrayaan-1 is ISRO's planned orbital mission to Venus:
        - Launch planned for December 2024
        - Will study Venus' surface and atmosphere
        - Carry 12 scientific instruments
        - Focus on atmospheric chemistry and surface mapping
        - Mission life of 4 years
        The mission aims to understand Venus' geological and atmospheric processes.'''
    },
    'nisar': {
        'pattern': r'nisar|nasa collaboration|earth observation satellite',
        'response': '''NISAR (NASA-ISRO Synthetic Aperture Radar):
        - Joint venture between NASA and ISRO
        - Launch planned for 2024
        - Will map entire Earth in 12 days
        - Monitor ecosystems, ice sheets, and natural hazards
        - Uses advanced radar imaging
        - Cost-effective solution for global earth observation'''
    },
    'space_station': {
        'pattern': r'space station|orbital platform|indian space station',
        'response': '''ISRO's Space Station Plans:
        - Plans for 20-tonne space station
        - To be launched in phases after Gaganyaan
        - Will support microgravity experiments
        - Planned orbit of 400km altitude
        - Focus on space tourism and research
        - Indigenous development and launch capability
        Expected to be operational by 2035.'''
    },
    'commercial': {
        'pattern': r'commercial|business|private sector|space economy',
        'response': '''ISRO's Commercial Activities:
        - NewSpace India Limited (NSIL) commercial arm
        - Launch services for international satellites
        - Technology transfer to industries
        - Satellite data services
        - Private sector participation in space
        - Support for space startups
        Contributing significantly to global space economy.'''
    },
    'scientists': {
        'pattern': r'scientist|vikram sarabhai|abdul kalam|k sivan|director',
        'response': '''Notable ISRO Scientists:
        - Dr. Vikram Sarabhai (Founder)
        - Dr. APJ Abdul Kalam (Missile Man)
        - Dr. Satish Dhawan (Former Chairman)
        - Dr. K Sivan (Former Chairman)
        - Dr. S Somanath (Current Chairman)
        Their contributions shaped India's space program.'''
    },
    'facilities': {
        'pattern': r'facility|center|laboratory|launch pad|sriharikota',
        'response': '''ISRO's Major Facilities:
        - Satish Dhawan Space Centre, Sriharikota (Launch center)
        - Space Applications Centre, Ahmedabad
        - Vikram Sarabhai Space Centre, Thiruvananthapuram
        - ISRO Satellite Centre, Bangalore
        - Liquid Propulsion Systems Centre
        - Physical Research Laboratory, Ahmedabad'''
    },
    'deep_space': {
        'pattern': r'deep space|interplanetary|solar system|exploration',
        'response': '''ISRO's Deep Space Missions:
        - Mars Orbiter Mission (Mangalyaan)
        - Chandrayaan series (Moon missions)
        - Aditya-L1 (Solar mission)
        - Future missions planned:
          * Shukrayaan-1 (Venus)
          * Mars Orbiter Mission 2
          * Jupiter mission studies'''
    },
    'climate': {
        'pattern': r'climate|environment|earth observation|weather',
        'response': '''ISRO's Climate Monitoring:
        - INSAT series for weather monitoring
        - OCEANSAT for ocean and atmospheric studies
        - SCATSAT-1 for weather forecasting
        - SARAL for sea surface studies
        - RESOURCESAT for resource monitoring
        Supporting climate change research and disaster management.'''
    },
    'navigation': {
        'pattern': r'navigation|navic|irnss|gps',
        'response': '''NavIC (Navigation with Indian Constellation):
        - India's indigenous GPS system
        - 8 satellites in orbit
        - Covers India and region up to 1500 km
        - Accuracy better than 20 meters
        - Applications in:
          * Transportation
          * Emergency services
          * Maritime operations
          * Telecommunications'''
    },
    'recovery': {
        'pattern': r'recovery|landing|reusable|return mission',
        'response': '''ISRO's Recovery Programs:
        - Space Capsule Recovery Experiment (SRE)
        - Reusable Launch Vehicle (RLV) program
        - Crew Module Atmospheric Re-entry Experiment
        - Pad Abort Test for Gaganyaan
        - Future plans for reusable rockets
        Developing capabilities for human spaceflight and cost reduction.'''
    }
}

def get_openai_response(query: str) -> str:
    """Get response from OpenAI API for unknown queries."""
    try:
        messages = [
            {"role": "system", "content": "You are ISRO Space Assistant, an AI expert on Indian space research and ISRO's activities. Provide detailed, accurate information about ISRO, space missions, and related topics. Keep responses concise but informative."},
            {"role": "user", "content": query}
        ]
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=300,
            temperature=0.7
        )
        
        return response.choices[0].message['content']
    except Exception as e:
        return f"I apologize, but I'm having trouble connecting to the knowledge base. Please try again later. Error: {str(e)}"

def get_chat_response(message: str) -> str:
    """Get response for user message using knowledge base or OpenAI."""
    message = message.lower().strip()
    
    # Score-based matching for better accuracy
    matches = []
    for topic, data in ISRO_KNOWLEDGE.items():
        pattern = data['pattern']
        # Find all matches in the message
        if re.findall(pattern, message):
            # Calculate match score based on number of words matched
            matched_words = len(re.findall(r'\w+', re.findall(pattern, message)[0]))
            total_words = len(message.split())
            score = matched_words / total_words
            matches.append((topic, score, data['response']))
    
    if matches:
        # Sort by score and get the best match
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches[0][2]
    
    # If no match found in knowledge base, use OpenAI
    return get_openai_response(message)

@app.route('/')
def home():
    return render_template('index.html')

# Explicitly serve static files (in case of issues)
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)
 
@app.route('/log_entry', methods=['GET', 'POST'])
def log_entry():
    if request.method == 'POST':
        name = request.form['name']
        role = request.form['role']
        college = request.form['college']
        mobile_number = request.form['mobile_number']  # ✅ fixed key
        email = request.form['email']
        total_students = request.form['total_students']  # ✅ fixed key
        total_faculties = request.form['total_faculties']  # ✅ fixed key
        feedback = request.form['feedback']
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")      # Get feedback ratings
        lecture_rating = request.form.get('Lecture_&_Interaction', '')
        display_rating = request.form.get('Display_&_Explanation', '')
        exhibition_rating = request.form.get('Exhibition_of_Models', '')
        video_rating = request.form.get('Video_Show', '')
        selfie_rating = request.form.get('Selfie_Corner', '')
        overall_rating = request.form.get('Overall_Arrangements', '')
        
        # Combine all data
        row = [
            timestamp, name, role, college, mobile_number, email, 
            total_students, total_faculties,
            lecture_rating, display_rating, exhibition_rating,
            video_rating, selfie_rating, overall_rating,
            feedback  # Additional comments
        ]
        
        headers = [
            'Timestamp', 'Name', 'Role', 'College', 'Mobile Number', 'Email',
            'Total Students', 'Total Faculties',
            'Lecture Rating', 'Display Rating', 'Exhibition Rating',
            'Video Rating', 'Selfie Rating', 'Overall Rating',
            'Additional Comments'
        ]
        
        append_to_excel('feedback.xlsx', row, headers)

        return redirect('/')
    return render_template('log_entry.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '').lower()
    
    # Get response from knowledge base
    reply = get_chat_response(message)
    
    return jsonify({
        'reply': reply
    })

@app.route('/bot')
def chatbot():
    return render_template('chatbot.html')

if __name__ == '__main__':
    app.run(debug=True)
