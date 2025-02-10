from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.units import inch
import random

# Configuration variables
TITLE = "Super Bowl Commercial Bingo"
INSTRUCTIONS = "The goal of almost all commercials is to convince you to think more highly of a brand. The grid below lists some of the messages or themes commercials use to try to influence us. When you see a commercial that uses one of the messages/themes below, write the name of the brand in the corresponding box. 1 box per commercial. Win by marking 5 boxes in a row (vertical, horizontal, or diagonal)."
NUM_PAGES = 30  # Will generate twice this many cards (2 per page)
CENTER_SQUARE = "Humor"

# List of persuasive techniques (excluding the center square technique)
TECHNIQUES = [
    '“Everyone is doing it!”',
    "Urgency (“Act now!”)",
    "Testimonials",
    "Promise of physical attractiveness",
    "Association with physical attractiveness",
    "Scarcity",
    '“Be part of the in-group”',
    "Nostalgia",
    "Promise of authenticity",
    "Fear of missing out",
    "Promise of being accepted",
    "Thrill-seeking",
    '“Be your own person”',
    '“Live for the moment”',
    "Promise of status",
    '“Impress others with your good taste”',
    '“You’re smarter than these people we’re all laughing at”',
    "Emotional storytelling",
    "Patriotism",
    "Value of family",
    "Environmental responsibility",
    "Social responsibility",
    "Celebrity credibility",
    "Celebrity association",
    "Solves a problem",
    "Better than competitor",
    "Scientific evidence",
    "Bang for the buck",
    "Promise of desirable lifestyle",
    "Tradition",
    '“Simplify your life”',
    '“Become the person you want to be”',
    "Envy",
    "Promise of safety / security",
    "Luxury / indulgence",
    "Promise of being more masculine / feminine",
    "Health / wellness",
    "“Be a trend-setter”",
    "Convenience",
    "Promise of success",
    "Association with success",
    "Self improvement",
    "Comfort / ease",
    '“Live for yourself, not anyone else”'
]

def create_bingo_card():
    # Select 24 random techniques (excluding center square)
    card_content = random.sample(TECHNIQUES, 24)
    
    # Create 5x5 grid with paragraphs for text wrapping
    grid = []
    index = 0
    for i in range(5):
        row = []
        for j in range(5):
            if i == 2 and j == 2:  # Center square
                content = CENTER_SQUARE
            else:
                content = card_content[index]
                index += 1
            # Add hyphenation points and wrap in Paragraph
            cell = Paragraph(content, cell_style)
            row.append(cell)
        grid.append(row)
    return grid

def create_single_card():
    # Create the grid
    grid = create_bingo_card()
    
    # Calculate dimensions for a portrait-oriented card
    card_width = 4.0 * inch  # Width of the card
    square_width = card_width / 5  # Width of each bingo square
    square_height = square_width * 1.2  # Make rectangles 20% taller than wide
    
    # Create the bingo grid
    bingo_table = Table(grid, 
                       colWidths=[square_width] * 5,
                       rowHeights=[square_height] * 5,
                       style=TableStyle([
                           ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                           ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                           ('GRID', (0,0), (-1,-1), 1, colors.black),
                           ('FONTSIZE', (0,0), (-1,-1), 8),
                           ('LEFTPADDING', (0,0), (-1,-1), 3),
                           ('RIGHTPADDING', (0,0), (-1,-1), 3),
                           ('TOPPADDING', (0,0), (-1,-1), 3),
                           ('BOTTOMPADDING', (0,0), (-1,-1), 3),
                       ]))
    
    # Create the complete card with title and instructions
    card_content = [
        [Paragraph(TITLE, title_style)],
        [Paragraph(INSTRUCTIONS, instruction_style)],
        [bingo_table]
    ]
    
    complete_card = Table(card_content,
                         colWidths=[card_width],
                         rowHeights=[0.5*inch, 1.4*inch, square_height * 5],
                         style=TableStyle([
                             ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                             ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                         ]))
    
    return complete_card

def create_pdf(filename):
    # Create the document with landscape orientation
    doc = SimpleDocTemplate(filename, 
                          pagesize=landscape(letter),
                          leftMargin=0.5*inch,
                          rightMargin=0.5*inch,
                          topMargin=0.5*inch,
                          bottomMargin=0.5*inch)
    
    elements = []
    
    # Create pages with two cards side by side
    for _ in range(NUM_PAGES):
        # Create a row with two cards and empty middle column for gutter
        card1 = create_single_card()
        card2 = create_single_card()
        
        # Put the cards side by side with gutter
        page_table = Table([[card1, '', card2]], 
                          colWidths=[4.0*inch, 1.5*inch, 4.0*inch],
                          style=TableStyle([
                              ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                              ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                              ('LEFTPADDING', (0,0), (-1,-1), 0.75*inch),
                              ('RIGHTPADDING', (0,0), (-1,-1), 0.75*inch),
                          ]))
        
        elements.append(page_table)
    
    doc.build(elements)

# Define styles
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=16,
    alignment=1,
    spaceAfter=6
)
instruction_style = ParagraphStyle(
    'CustomInstructions',
    parent=styles['Normal'],
    fontSize=10,
    alignment=0,
    spaceAfter=6,
    xml=1  # This enables HTML tags
)
cell_style = ParagraphStyle(
    'CellStyle',
    parent=styles['Normal'],
    fontSize=8,
    alignment=1,
    leading=9,  # Controls line spacing within cells
    wordWrap='LTR',  # Left-to-right text wrapping
    allowWidows=0,
    allowOrphans=0,
    splitLongWords=1,  # Enable word splitting
    hyphenationLanguage='en_US',  # Note: hyphenationLanguage, not hyphenationLang
    hyphenationMinWordLength=5,
    hyphenationRemainCharLength=2,  # Minimum chars before hyphen
    hyphenationCharLength=2  # Minimum chars after hyphen
)

if __name__ == "__main__":
    create_pdf("bingo_cards.pdf")
    print("PDF generated successfully!")