from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.units import inch
import random

# Configuration variables
TITLE = "Super Bowl Commercial BINGO"
INSTRUCTIONS = "Mark off each persuasive technique as you see it used in Super Bowl commercials!"
NUM_PAGES = 20  # Will generate twice this many cards (2 per page)
CENTER_SQUARE = "Humor as persuasion"

# List of persuasive techniques (excluding the center square technique)
TECHNIQUES = [
    "Bandwagon effect",
    "Social proof through testimonials",
    "Authority appeal",
    "Scarcity appeal",
    "Exclusivity appeal",
    "Nostalgia appeal",
    "Fear appeal",
    "FOMO",
    "Status/prestige appeal",
    "Emotional storytelling appeal",
    "Patriotic appeal",
    "Family values appeal",
    "Environmental responsibility appeal",
    "Social responsibility appeal",
    "Celebrity credibility appeal",
    "Problem-solution framework",
    "Comparative advantage",
    "Scientific/statistical evidence",
    "Value proposition",
    "Lifestyle association",
    "Tradition/heritage appeal",
    "Simplification appeal",
    "Peer pressure appeal",
    "Aspirational appeal",
    "Guilt appeal",
    "Safety/security appeal",
    "Luxury/indulgence appeal",
    "Masculinity/femininity appeal",
    "Health/wellness appeal",
    "Innovation/cutting-edge appeal",
    "Convenience appeal",
    "Unity/belonging appeal",
    "Success association",
    "Self-improvement appeal"
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
            # Wrap each cell's content in a Paragraph for text wrapping
            cell = Paragraph(content, cell_style)
            row.append(cell)
        grid.append(row)
    return grid

def create_single_card():
    # Create the grid
    grid = create_bingo_card()
    
    # Calculate dimensions for a portrait-oriented card
    card_width = 4.0 * inch  # Width of the card
    square_size = card_width / 5  # Size of each bingo square
    
    # Create the bingo grid
    bingo_table = Table(grid, 
                       colWidths=[square_size] * 5,
                       rowHeights=[square_size] * 5,
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
                         rowHeights=[0.4*inch, 0.3*inch, card_width],
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
        # Create a row with two cards
        card1 = create_single_card()
        card2 = create_single_card()
        
        # Put the cards side by side in a table with spacing between them
        page_table = Table([[card1, '', card2]], 
                  colWidths=[4.0*inch, 1.0*inch, 4.0*inch],
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
    alignment=1,
    spaceAfter=6
)
cell_style = ParagraphStyle(
    'CellStyle',
    parent=styles['Normal'],
    fontSize=8,
    alignment=1,
    leading=9,  # Controls line spacing within cells
    wordWrap='CJK'  # Ensures aggressive word wrapping
)

if __name__ == "__main__":
    create_pdf("bingo_cards.pdf")
    print("PDF generated successfully!")