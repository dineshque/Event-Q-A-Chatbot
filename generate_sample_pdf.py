from fpdf import FPDF
import os

class EventPDF(FPDF):
    def __init__(self):
        super().__init__()
        # Set UTF-8 encoding for better Unicode support
        self.set_auto_page_break(auto=True, margin=15)
    
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.set_text_color(0, 51, 102)
        self.cell(0, 15, 'TechConf 2024 - AI & Machine Learning Summit', 0, 1, 'C')
        self.set_text_color(0, 0, 0)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def safe_text(self, text):
        """Clean text to remove problematic Unicode characters"""
        # Replace bullet points and other Unicode characters
        replacements = {
            '\u2022': '- ',  # Bullet point
            '\u2013': '-',   # En dash
            '\u2014': '--',  # Em dash
            '\u2018': "'",   # Left single quote
            '\u2019': "'",   # Right single quote
            '\u201c': '"',   # Left double quote
            '\u201d': '"',   # Right double quote
        }
        
        for unicode_char, replacement in replacements.items():
            text = text.replace(unicode_char, replacement)
        
        return text

    def body_text(self, text):
        self.set_font('Arial', '', 11)
        clean_text = self.safe_text(text)
        self.multi_cell(0, 6, clean_text)
        self.ln(3)

def clean_text_for_pdf(text):
    """Remove or replace Unicode characters that cause encoding issues"""
    # Replace common Unicode characters
    replacements = {
        '\u2022': '- ',      # Bullet point
        '\u2013': '-',       # En dash  
        '\u2014': '--',      # Em dash
        '\u2018': "'",       # Left single quote
        '\u2019': "'",       # Right single quote
        '\u201c': '"',       # Left double quote
        '\u201d': '"',       # Right double quote
        '\u2026': '...',     # Ellipsis
        '\u00a0': ' ',       # Non-breaking space
    }
    
    for unicode_char, replacement in replacements.items():
        text = text.replace(unicode_char, replacement)
    
    # Remove any remaining non-latin1 characters
    text = text.encode('latin-1', errors='ignore').decode('latin-1')
    
    return text

# Apply this function to all text before adding to PDF
def create_safe_event_pdf():
    pdf = EventPDF()
    pdf.add_page()
    
    # Clean all text content
    event_overview = clean_text_for_pdf('''Welcome to TechConf 2024, the premier AI & Machine Learning Summit bringing together industry leaders, researchers, and innovators from around the globe...''')
    
    pdf.body_text(event_overview)
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def create_event_pdf_reportlab():
    doc = SimpleDocTemplate("sample_event_reportlab.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor='darkblue',
        alignment=1  # Center alignment
    )
    
    story.append(Paragraph("TechConf 2024 - AI & Machine Learning Summit", title_style))
    story.append(Spacer(1, 12))
    
    # Content with Unicode support
    content = """
    Welcome to TechConf 2024, featuring:
    • Keynote speakers from leading tech companies
    • Hands-on workshops and technical sessions  
    • Networking opportunities with industry experts
    • Latest advances in AI and machine learning
    """
    
    story.append(Paragraph(content, styles['Normal']))
    
    doc.build(story)
    return "sample_event_reportlab.pdf"

def create_comprehensive_event_pdf():
    pdf = EventPDF()
    
    # Page 1: Event Overview
    pdf.add_page()
    
    pdf.set_title('EVENT OVERVIEW')
    pdf.body_text('''Welcome to TechConf 2024, the premier AI & Machine Learning Summit bringing together industry leaders, researchers, and innovators from around the globe. This two-day conference will feature cutting-edge presentations, hands-on workshops, and networking opportunities.

Date: June 15-16, 2024
Venue: San Francisco Convention Center
Expected Attendees: 2,500+ professionals
Registration Fee: $299 (Early Bird), $399 (Regular)''')

    pdf.set_title('KEYNOTE SPEAKERS')
    
    pdf.speaker_bio(
        "Dr. Sarah Chen",
        "AI Research Director",
        "Google DeepMind",
        "Dr. Chen leads Google's advanced AI research initiatives with over 15 years of experience in machine learning and neural networks. She holds a PhD from MIT and has published over 100 papers in top-tier conferences. Her recent work focuses on large language models and their applications in healthcare."
    )
    
    pdf.speaker_bio(
        "Prof. Michael Rodriguez",
        "Professor of Computer Science",
        "Stanford University",
        "Professor Rodriguez is a renowned expert in computer vision and robotics. He directs the Stanford AI Lab and has been instrumental in developing breakthrough algorithms for autonomous vehicles. His research has been cited over 25,000 times and he holds 30+ patents."
    )
    
    pdf.speaker_bio(
        "Lisa Wang",
        "Chief Technology Officer",
        "OpenAI",
        "Lisa Wang oversees OpenAI's technical strategy and product development. She previously led engineering teams at Tesla and SpaceX, bringing extensive experience in scaling AI systems. She's a strong advocate for responsible AI development and deployment."
    )

    # Page 2: Detailed Agenda
    pdf.add_page()
    
    pdf.set_title('DETAILED AGENDA')
    
    pdf.subset_title('Day 1 - June 15, 2024')
    pdf.body_text('''8:00 AM - 9:00 AM: Registration & Welcome Coffee
Location: Main Lobby

9:00 AM - 9:15 AM: Opening Remarks
Speaker: Conference Chair Dr. James Wilson
Location: Main Auditorium

9:15 AM - 10:15 AM: Keynote - "The Future of AI: Opportunities and Challenges"
Speaker: Dr. Sarah Chen (Google DeepMind)
Location: Main Auditorium
Description: Explore the latest developments in AI research and their potential impact on society, business, and technology.

10:15 AM - 10:45 AM: Coffee Break & Networking
Location: Exhibition Hall

10:45 AM - 12:00 PM: Workshop - "Building Production-Ready RAG Applications"
Instructor: Dr. Alex Kumar (Microsoft Research)
Location: Workshop Room A
Prerequisites: Basic Python knowledge
Description: Hands-on workshop covering retrieval-augmented generation systems, vector databases, and deployment strategies.

12:00 PM - 1:30 PM: Lunch & Sponsor Presentations
Location: Main Hall

1:30 PM - 2:30 PM: Panel Discussion - "Ethics in AI Development"
Moderator: Prof. Maria Santos (Berkeley)
Panelists: Dr. Sarah Chen, Lisa Wang, Dr. Robert Kim (IBM)
Location: Main Auditorium

2:30 PM - 3:30 PM: Technical Session - "Advances in Natural Language Processing"
Speakers: Multiple researchers presenting 15-minute talks
Location: Conference Room B

3:30 PM - 4:00 PM: Afternoon Break
Location: Exhibition Hall

4:00 PM - 5:00 PM: Industry Showcase - "AI in Healthcare"
Speakers: Representatives from leading healthcare AI companies
Location: Main Auditorium

5:00 PM - 7:00 PM: Welcome Reception & Networking
Location: Rooftop Terrace''')

    # Page 3: Day 2 Agenda and Workshops
    pdf.add_page()
    
    pdf.subset_title('Day 2 - June 16, 2024')
    pdf.body_text('''9:00 AM - 10:00 AM: Keynote - "Computer Vision: From Research to Real-World Applications"
Speaker: Prof. Michael Rodriguez (Stanford University)
Location: Main Auditorium

10:00 AM - 10:30 AM: Coffee Break
Location: Exhibition Hall

10:30 AM - 12:00 PM: Workshop - "LLM Fine-tuning and Optimization"
Instructor: Dr. Jennifer Lee (Hugging Face)
Location: Workshop Room A
Prerequisites: Experience with transformers and PyTorch
Description: Learn advanced techniques for fine-tuning large language models for specific tasks and domains.

12:00 PM - 1:30 PM: Lunch & Poster Session
Location: Main Hall

1:30 PM - 2:30 PM: Fireside Chat - "The Business of AI"
Speakers: Lisa Wang (OpenAI) & Mark Thompson (Andreessen Horowitz)
Location: Main Auditorium

2:30 PM - 3:30 PM: Technical Session - "MLOps and AI Infrastructure"
Location: Conference Room B

3:30 PM - 4:00 PM: Final Coffee Break
Location: Exhibition Hall

4:00 PM - 5:00 PM: Closing Keynote - "AI's Role in Solving Global Challenges"
Speaker: Dr. Priya Patel (UN AI Advisory Board)
Location: Main Auditorium

5:00 PM - 5:30 PM: Closing Remarks & Awards Ceremony
Location: Main Auditorium''')

    pdf.set_title('WORKSHOP DETAILS')
    
    pdf.subset_title('Workshop 1: Building Production-Ready RAG Applications')
    pdf.body_text('''Instructor: Dr. Alex Kumar, Senior Research Scientist at Microsoft Research
Duration: 75 minutes
Capacity: 50 participants
Requirements: Laptop with Python 3.8+, basic ML knowledge

What you'll learn:
• Understanding RAG architecture and components
• Implementing vector databases for document retrieval
• Integrating large language models for response generation
• Best practices for production deployment
• Handling edge cases and error scenarios

Materials provided:
• Complete code repository
• Sample datasets
• Deployment templates
• Reference documentation''')

    pdf.subset_title('Workshop 2: LLM Fine-tuning and Optimization')
    pdf.body_text('''Instructor: Dr. Jennifer Lee, ML Engineer at Hugging Face
Duration: 90 minutes
Capacity: 40 participants
Requirements: GPU-enabled laptop or cloud credits provided

What you'll learn:
• Parameter-efficient fine-tuning techniques (LoRA, AdaLoRA)
• Dataset preparation and preprocessing
• Training monitoring and evaluation
• Model compression and quantization
• Deployment optimization strategies

Hands-on exercises:
• Fine-tune a model for sentiment analysis
• Implement custom training loops
• Compare different optimization techniques
• Deploy optimized models''')

    # Page 4: Venue and Logistics
    pdf.add_page()
    
    pdf.set_title('VENUE INFORMATION')
    pdf.body_text('''San Francisco Convention Center
747 Howard Street, San Francisco, CA 94103

The San Francisco Convention Center is a state-of-the-art facility located in the heart of SOMA district. The venue features:
• High-speed WiFi throughout the facility
• Multiple presentation rooms with AV equipment
• Accessible facilities and accommodations
• On-site catering and coffee stations
• Parking garage with 1,500+ spaces

Transportation:
• BART: Montgomery Street Station (0.5 miles)
• Muni: Multiple bus lines serve the area
• Ride-sharing pickup/drop-off zones available
• Bike parking facilities on-site''')

    pdf.set_title('ACCOMMODATION RECOMMENDATIONS')
    pdf.body_text('''Partner Hotels (Special Conference Rates):

Marriott Marquis San Francisco
Distance: 0.2 miles walking
Rate: $189/night (mention TechConf 2024)
Amenities: Pool, fitness center, multiple restaurants

Hotel Zephyr San Francisco
Distance: 1.5 miles
Rate: $159/night
Amenities: Unique nautical theme, waterfront location

The Westin San Francisco Market Street
Distance: 0.8 miles
Rate: $199/night
Amenities: Luxury amenities, spa services

Budget Options:
• HI San Francisco Downtown Hostel ($45/night)
• Beck's Motor Lodge ($89/night)
• Various Airbnb options in the area''')

    pdf.set_title('SPONSORS & PARTNERS')
    pdf.body_text('''Platinum Sponsors:
• Google Cloud - Providing cloud credits for workshop participants
• Microsoft Azure - Supporting the AI infrastructure track
• NVIDIA - Powering our GPU-intensive workshops

Gold Sponsors:
• Hugging Face - Open source AI platform
• Weights & Biases - ML experiment tracking
• Pinecone - Vector database solutions

Silver Sponsors:
• Cohere - Language AI platform
• Anthropic - AI safety research
• Scale AI - Data platform for AI

Community Partners:
• AI/ML San Francisco Meetup
• Women in AI
• Stanford AI Lab
• UC Berkeley AI Research''')

    # Save the PDF
    output_path = 'sample_event_comprehensive.pdf'
    pdf.output(output_path)
    return output_path

# Generate the PDF
if __name__ == "__main__":
    pdf_path = create_comprehensive_event_pdf()
    print(f"Comprehensive sample PDF created: {pdf_path}")
