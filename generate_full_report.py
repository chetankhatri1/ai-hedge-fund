import os
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'AI Hedge Fund Analysis Report', 0, 1, 'C')
        self.ln(5)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

# Create PDF
pdf = PDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)

# Add date
pdf.set_font('Arial', 'I', 10)
pdf.cell(0, 10, 'March 26, 2025', 0, 1, 'R')
pdf.ln(5)

# Executive Summary
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, 'Executive Summary', 0, 1, 'L')
pdf.set_font('Arial', '', 10)
pdf.multi_cell(0, 5, 'This report presents the analysis and trading recommendations generated by the AI Hedge Fund system for three major technology stocks: AAPL, MSFT, and NVDA. The analysis incorporates insights from multiple AI analysts, each with a unique investment philosophy and approach.')
pdf.ln(5)

# Portfolio Summary
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, 'Portfolio Summary', 0, 1, 'L')

# Table header
pdf.set_font('Arial', 'B', 10)
pdf.set_fill_color(240, 240, 240)
pdf.cell(40, 7, 'Ticker', 1, 0, 'C', True)
pdf.cell(40, 7, 'Action', 1, 0, 'C', True)
pdf.cell(40, 7, 'Quantity', 1, 0, 'C', True)
pdf.cell(40, 7, 'Confidence', 1, 1, 'C', True)

# Table data
pdf.set_font('Arial', '', 10)
# AAPL
pdf.cell(40, 7, 'AAPL', 1, 0, 'C')
pdf.set_text_color(231, 76, 60)  # Red for SHORT
pdf.cell(40, 7, 'SHORT', 1, 0, 'C')
pdf.set_text_color(0, 0, 0)  # Reset to black
pdf.cell(40, 7, '50', 1, 0, 'C')
pdf.cell(40, 7, '65.0%', 1, 1, 'C')
# MSFT
pdf.cell(40, 7, 'MSFT', 1, 0, 'C')
pdf.set_text_color(52, 152, 219)  # Blue for HOLD
pdf.cell(40, 7, 'HOLD', 1, 0, 'C')
pdf.set_text_color(0, 0, 0)  # Reset to black
pdf.cell(40, 7, '0', 1, 0, 'C')
pdf.cell(40, 7, '55.0%', 1, 1, 'C')
# NVDA
pdf.cell(40, 7, 'NVDA', 1, 0, 'C')
pdf.set_text_color(52, 152, 219)  # Blue for HOLD
pdf.cell(40, 7, 'HOLD', 1, 0, 'C')
pdf.set_text_color(0, 0, 0)  # Reset to black
pdf.cell(40, 7, '0', 1, 0, 'C')
pdf.cell(40, 7, '60.0%', 1, 1, 'C')
pdf.ln(5)

# Portfolio Strategy
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, 'Portfolio Strategy', 0, 1, 'L')
pdf.set_font('Arial', '', 10)
pdf.multi_cell(0, 5, 'Multiple high-confidence bearish signals from valuation (76%), Cathie Wood (72%), Warren Buffett (75%), and sentiment (59%) suggest AAPL is overvalued. No strong bullish signals counter this perspective. Initiating a moderate short position to capitalize on potential downside while managing risk.')
pdf.ln(5)

# Analysis for AAPL
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, 'Detailed Analysis: AAPL', 0, 1, 'L')

# AAPL Agent Analysis Table
pdf.set_font('Arial', 'B', 10)
pdf.set_fill_color(240, 240, 240)
pdf.cell(60, 7, 'Agent', 1, 0, 'C', True)
pdf.cell(30, 7, 'Signal', 1, 0, 'C', True)
pdf.cell(30, 7, 'Confidence', 1, 0, 'C', True)
pdf.cell(70, 7, 'Reasoning', 1, 1, 'C', True)

# AAPL Agent Analysis Data
pdf.set_font('Arial', '', 9)

# Ben Graham
pdf.cell(60, 7, 'Ben Graham', 1, 0, 'L')
pdf.set_text_color(231, 76, 60)  # Red for SELL
pdf.cell(30, 7, 'SELL', 1, 0, 'C')
pdf.set_text_color(0, 0, 0)  # Reset to black
pdf.cell(30, 7, '65%', 1, 0, 'C')
pdf.multi_cell(70, 7, 'P/E ratio of 33 exceeds margin of safety threshold. Current price significantly above book value.', 1, 'L')

# Bill Ackman
pdf.cell(60, 7, 'Bill Ackman', 1, 0, 'L')
pdf.set_text_color(231, 76, 60)  # Red for SELL
pdf.cell(30, 7, 'SELL', 1, 0, 'C')
pdf.set_text_color(0, 0, 0)  # Reset to black
pdf.cell(30, 7, '70%', 1, 0, 'C')
pdf.multi_cell(70, 7, 'Limited growth catalysts and increasing competition in key markets.', 1, 'L')

# Warren Buffett
pdf.cell(60, 7, 'Warren Buffett', 1, 0, 'L')
pdf.set_text_color(231, 76, 60)  # Red for SELL
pdf.cell(30, 7, 'SELL', 1, 0, 'C')
pdf.set_text_color(0, 0, 0)  # Reset to black
pdf.cell(30, 7, '75%', 1, 0, 'C')
pdf.multi_cell(70, 7, 'Current valuation exceeds intrinsic value. Declining iPhone market share.', 1, 'L')

# Cathie Wood
pdf.cell(60, 7, 'Cathie Wood', 1, 0, 'L')
pdf.set_text_color(231, 76, 60)  # Red for SELL
pdf.cell(30, 7, 'SELL', 1, 0, 'C')
pdf.set_text_color(0, 0, 0)  # Reset to black
pdf.cell(30, 7, '72%', 1, 0, 'C')
pdf.multi_cell(70, 7, 'Insufficient innovation pipeline to justify current valuation.', 1, 'L')

# Valuation
pdf.cell(60, 7, 'Valuation', 1, 0, 'L')
pdf.set_text_color(231, 76, 60)  # Red for SELL
pdf.cell(30, 7, 'SELL', 1, 0, 'C')
pdf.set_text_color(0, 0, 0)  # Reset to black
pdf.cell(30, 7, '76%', 1, 0, 'C')
pdf.multi_cell(70, 7, 'DCF model indicates 15% overvaluation based on projected cash flows.', 1, 'L')

# Sentiment
pdf.cell(60, 7, 'Sentiment', 1, 0, 'L')
pdf.set_text_color(231, 76, 60)  # Red for SELL
pdf.cell(30, 7, 'SELL', 1, 0, 'C')
pdf.set_text_color(0, 0, 0)  # Reset to black
pdf.cell(30, 7, '59%', 1, 0, 'C')
pdf.multi_cell(70, 7, 'Negative sentiment trends in social media and analyst reports.', 1, 'L')

# AAPL Trading Decision
pdf.ln(5)
pdf.set_font('Arial', 'B', 11)
pdf.cell(0, 7, 'Trading Decision for AAPL', 0, 1, 'L')

pdf.set_font('Arial', 'B', 10)
pdf.set_fill_color(240, 240, 240)
pdf.cell(40, 7, 'Action', 1, 0, 'L', True)
pdf.set_font('Arial', '', 10)
pdf.set_text_color(231, 76, 60)  # Red for SHORT
pdf.cell(120, 7, 'SHORT', 1, 1, 'L')
pdf.set_text_color(0, 0, 0)  # Reset to black

pdf.set_font('Arial', 'B', 10)
pdf.cell(40, 7, 'Quantity', 1, 0, 'L', True)
pdf.set_font('Arial', '', 10)
pdf.cell(120, 7, '50', 1, 1, 'L')

pdf.set_font('Arial', 'B', 10)
pdf.cell(40, 7, 'Confidence', 1, 0, 'L', True)
pdf.set_font('Arial', '', 10)
pdf.cell(120, 7, '65.0%', 1, 1, 'L')

pdf.set_font('Arial', 'B', 10)
pdf.cell(40, 7, 'Reasoning', 1, 0, 'L', True)
pdf.set_font('Arial', '', 10)
pdf.multi_cell(120, 7, 'Multiple high-confidence bearish signals from valuation (76%), Cathie Wood (72%), Warren Buffett (75%), and sentiment (59%) suggest AAPL is overvalued. No strong bullish signals to counter this perspective.', 1, 'L')

# Analysis for MSFT
pdf.add_page()
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, 'Detailed Analysis: MSFT', 0, 1, 'L')

# MSFT Agent Analysis Table
pdf.set_font('Arial', 'B', 10)
pdf.set_fill_color(240, 240, 240)
pdf.cell(60, 7, 'Agent', 1, 0, 'C', True)
pdf.cell(30, 7, 'Signal', 1, 0, 'C', True)
pdf.cell(30, 7, 'Confidence', 1, 0, 'C', True)
pdf.cell(70, 7, 'Reasoning', 1, 1, 'C', True)

# MSFT Agent Analysis Data
pdf.set_font('Arial', '', 9)

# Ben Graham
pdf.cell(60, 7, 'Ben Graham', 1, 0, 'L')
pdf.set_text_color(46, 204, 113)  # Green for BUY
pdf.cell(30, 7, 'BUY', 1, 0, 'C')
pdf.set_text_color(0, 0, 0)  # Reset to black
pdf.cell(30, 7, '60%', 1, 0, 'C')
pdf.multi_cell(70, 7, 'Strong balance sheet with consistent cash flow generation.', 1, 'L')

# Charlie Munger
pdf.cell(60, 7, 'Charlie Munger', 1, 0, 'L')
pdf.set_text_color(46, 204, 113)  # Green for BUY
pdf.cell(30, 7, 'BUY', 1, 0, 'C')
pdf.set_text_color(0, 0, 0)  # Reset to black
pdf.cell(30, 7, '65%', 1, 0, 'C')
pdf.multi_cell(70, 7, 'Dominant market position with strong competitive moat in cloud services.', 1, 'L')

# Fundamentals
pdf.cell(60, 7, 'Fundamentals', 1, 0, 'L')
pdf.set_text_color(46, 204, 113)  # Green for BUY
pdf.cell(30, 7, 'BUY', 1, 0, 'C')
pdf.set_text_color(0, 0, 0)  # Reset to black
pdf.cell(30, 7, '70%', 1, 0, 'C')
pdf.multi_cell(70, 7, 'Strong revenue growth in cloud and AI segments.', 1, 'L')

# Bill Ackman
pdf.cell(60, 7, 'Bill Ackman', 1, 0, 'L')
pdf.set_text_color(231, 76, 60)  # Red for SELL
pdf.cell(30, 7, 'SELL', 1, 0, 'C')
pdf.set_text_color(0, 0, 0)  # Reset to black
pdf.cell(30, 7, '55%', 1, 0, 'C')
pdf.multi_cell(70, 7, 'Concerns about regulatory headwinds and antitrust scrutiny.', 1, 'L')

# Valuation
pdf.cell(60, 7, 'Valuation', 1, 0, 'L')
pdf.set_text_color(231, 76, 60)  # Red for SELL
pdf.cell(30, 7, 'SELL', 1, 0, 'C')
pdf.set_text_color(0, 0, 0)  # Reset to black
pdf.cell(30, 7, '60%', 1, 0, 'C')
pdf.multi_cell(70, 7, 'Current valuation appears stretched relative to historical averages.', 1, 'L')

# Technical Analyst
pdf.cell(60, 7, 'Technical Analyst', 1, 0, 'L')
pdf.set_text_color(231, 76, 60)  # Red for SELL
pdf.cell(30, 7, 'SELL', 1, 0, 'C')
pdf.set_text_color(0, 0, 0)  # Reset to black
pdf.cell(30, 7, '65%', 1, 0, 'C')
pdf.multi_cell(70, 7, 'Bearish technical patterns forming with declining volume.', 1, 'L')

# MSFT Trading Decision
pdf.ln(5)
pdf.set_font('Arial', 'B', 11)
pdf.cell(0, 7, 'Trading Decision for MSFT', 0, 1, 'L')

pdf.set_font('Arial', 'B', 10)
pdf.set_fill_color(240, 240, 240)
pdf.cell(40, 7, 'Action', 1, 0, 'L', True)
pdf.set_font('Arial', '', 10)
pdf.set_text_color(52, 152, 219)  # Blue for HOLD
pdf.cell(120, 7, 'HOLD', 1, 1, 'L')
pdf.set_text_color(0, 0, 0)  # Reset to black

pdf.set_font('Arial', 'B', 10)
pdf.cell(40, 7, 'Quantity', 1, 0, 'L', True)
pdf.set_font('Arial', '', 10)
pdf.cell(120, 7, '0', 1, 1, 'L')

pdf.set_font('Arial', 'B', 10)
pdf.cell(40, 7, 'Confidence', 1, 0, 'L', True)
pdf.set_font('Arial', '', 10)
pdf.cell(120, 7, '55.0%', 1, 1, 'L')

pdf.set_font('Arial', 'B', 10)
pdf.cell(40, 7, 'Reasoning', 1, 0, 'L', True)
pdf.set_font('Arial', '', 10)
pdf.multi_cell(120, 7, 'Mixed signals with strong fundamental indicators but concerning technical and valuation metrics. Low confidence in either direction suggests maintaining current position.', 1, 'L')

# Analysis for NVDA
pdf.add_page()
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, 'Detailed Analysis: NVDA', 0, 1, 'L')

# NVDA Agent Analysis Table
pdf.set_font('Arial', 'B', 10)
pdf.set_fill_color(240, 240, 240)
pdf.cell(60, 7, 'Agent', 1, 0, 'C', True)
pdf.cell(30, 7, 'Signal', 1, 0, 'C', True)
pdf.cell(30, 7, 'Confidence', 1, 0, 'C', True)
pdf.cell(70, 7, 'Reasoning', 1, 1, 'C', True)

# NVDA Agent Analysis Data
pdf.set_font('Arial', '', 9)

# Cathie Wood
pdf.cell(60, 7, 'Cathie Wood', 1, 0, 'L')
pdf.set_text_color(46, 204, 113)  # Green for BUY
pdf.cell(30, 7, 'BUY', 1, 0, 'C')
pdf.set_text_color(0, 0, 0)  # Reset to black
pdf.cell(30, 7, '85%', 1, 0, 'C')
pdf.multi_cell(70, 7, 'Leading position in AI and data center markets with exponential growth potential.', 1, 'L')

# Phil Fisher
pdf.cell(60, 7, 'Phil Fisher', 1, 0, 'L')
pdf.set_text_color(46, 204, 113)  # Green for BUY
pdf.cell(30, 7, 'BUY', 1, 0, 'C')
pdf.set_text_color(0, 0, 0)  # Reset to black
pdf.cell(30, 7, '78%', 1, 0, 'C')
pdf.multi_cell(70, 7, 'Strong management team with clear vision and execution in growth markets.', 1, 'L')

# Stanley Druckenmiller
pdf.cell(60, 7, 'Stanley Druckenmiller', 1, 0, 'L')
pdf.set_text_color(46, 204, 113)  # Green for BUY
pdf.cell(30, 7, 'BUY', 1, 0, 'C')
pdf.set_text_color(0, 0, 0)  # Reset to black
pdf.cell(30, 7, '80%', 1, 0, 'C')
pdf.multi_cell(70, 7, 'Asymmetric upside potential in AI revolution with strong market position.', 1, 'L')

# Bill Ackman
pdf.cell(60, 7, 'Bill Ackman', 1, 0, 'L')
pdf.set_text_color(231, 76, 60)  # Red for SELL
pdf.cell(30, 7, 'SELL', 1, 0, 'C')
pdf.set_text_color(0, 0, 0)  # Reset to black
pdf.cell(30, 7, '85%', 1, 0, 'C')
pdf.multi_cell(70, 7, 'Extreme valuation with unrealistic growth expectations already priced in.', 1, 'L')

# Warren Buffett
pdf.cell(60, 7, 'Warren Buffett', 1, 0, 'L')
pdf.set_text_color(231, 76, 60)  # Red for SELL
pdf.cell(30, 7, 'SELL', 1, 0, 'C')
pdf.set_text_color(0, 0, 0)  # Reset to black
pdf.cell(30, 7, '85%', 1, 0, 'C')
pdf.multi_cell(70, 7, 'Current price far exceeds intrinsic value with cyclical risks in semiconductor industry.', 1, 'L')

# Valuation
pdf.cell(60, 7, 'Valuation', 1, 0, 'L')
pdf.set_text_color(231, 76, 60)  # Red for SELL
pdf.cell(30, 7, 'SELL', 1, 0, 'C')
pdf.set_text_color(0, 0, 0)  # Reset to black
pdf.cell(30, 7, '75%', 1, 0, 'C')
pdf.multi_cell(70, 7, 'P/E ratio of 80+ indicates significant overvaluation even with strong growth.', 1, 'L')

# Sentiment
pdf.cell(60, 7, 'Sentiment', 1, 0, 'L')
pdf.set_text_color(231, 76, 60)  # Red for SELL
pdf.cell(30, 7, 'SELL', 1, 0, 'C')
pdf.set_text_color(0, 0, 0)  # Reset to black
pdf.cell(30, 7, '72%', 1, 0, 'C')
pdf.multi_cell(70, 7, 'Excessive bullish sentiment suggests contrarian opportunity to the downside.', 1, 'L')

# NVDA Trading Decision
pdf.ln(5)
pdf.set_font('Arial', 'B', 11)
pdf.cell(0, 7, 'Trading Decision for NVDA', 0, 1, 'L')

pdf.set_font('Arial', 'B', 10)
pdf.set_fill_color(240, 240, 240)
pdf.cell(40, 7, 'Action', 1, 0, 'L', True)
pdf.set_font('Arial', '', 10)
pdf.set_text_color(52, 152, 219)  # Blue for HOLD
pdf.cell(120, 7, 'HOLD', 1, 1, 'L')
pdf.set_text_color(0, 0, 0)  # Reset to black

pdf.set_font('Arial', 'B', 10)
pdf.cell(40, 7, 'Quantity', 1, 0, 'L', True)
pdf.set_font('Arial', '', 10)
pdf.cell(120, 7, '0', 1, 1, 'L')

pdf.set_font('Arial', 'B', 10)
pdf.cell(40, 7, 'Confidence', 1, 0, 'L', True)
pdf.set_font('Arial', '', 10)
pdf.cell(120, 7, '60.0%', 1, 1, 'L')

pdf.set_font('Arial', 'B', 10)
pdf.cell(40, 7, 'Reasoning', 1, 0, 'L', True)
pdf.set_font('Arial', '', 10)
reasoning_text = 'Highly polarized signals with strong bullish views from Cathie Wood (85%), Phil Fisher (78%), and Druckenmiller (80%), countered by equally strong bearish signals from Bill Ackman (85%), Warren Buffett (85%), valuation (75%), and sentiment (72%). This extreme divergence indicates high volatility risk and suggests waiting for consensus to emerge.'
pdf.multi_cell(120, 7, reasoning_text, 1, 'L')

# Add a page for methodology and AI analysts
pdf.add_page()

# AI Analysts
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, 'AI Analysts Contributing to This Analysis', 0, 1, 'L')
pdf.set_font('Arial', '', 10)

# Create a table for analysts with their investment philosophies
pdf.set_font('Arial', 'B', 10)
pdf.set_fill_color(240, 240, 240)
pdf.cell(60, 7, 'Analyst', 1, 0, 'C', True)
pdf.cell(130, 7, 'Investment Philosophy', 1, 1, 'C', True)

pdf.set_font('Arial', '', 9)
pdf.cell(60, 7, 'Ben Graham', 1, 0, 'L')
pdf.multi_cell(130, 7, 'The godfather of value investing, only buys hidden gems with a margin of safety', 1, 'L')

pdf.cell(60, 7, 'Bill Ackman', 1, 0, 'L')
pdf.multi_cell(130, 7, 'An activist investor who takes bold positions and pushes for change', 1, 'L')

pdf.cell(60, 7, 'Cathie Wood', 1, 0, 'L')
pdf.multi_cell(130, 7, 'The queen of growth investing, believes in the power of innovation and disruption', 1, 'L')

pdf.cell(60, 7, 'Charlie Munger', 1, 0, 'L')
pdf.multi_cell(130, 7, 'Warren Buffett\'s partner, only buys wonderful businesses at fair prices', 1, 'L')

pdf.cell(60, 7, 'Phil Fisher', 1, 0, 'L')
pdf.multi_cell(130, 7, 'Legendary growth investor who mastered scuttlebutt analysis', 1, 'L')

pdf.cell(60, 7, 'Stanley Druckenmiller', 1, 0, 'L')
pdf.multi_cell(130, 7, 'Macro legend who hunts for asymmetric opportunities with growth potential', 1, 'L')

pdf.cell(60, 7, 'Warren Buffett', 1, 0, 'L')
pdf.multi_cell(130, 7, 'The oracle of Omaha, seeks wonderful companies at a fair price', 1, 'L')

pdf.cell(60, 7, 'Valuation Agent', 1, 0, 'L')
pdf.multi_cell(130, 7, 'Calculates the intrinsic value of a stock and generates trading signals', 1, 'L')

pdf.cell(60, 7, 'Sentiment Agent', 1, 0, 'L')
pdf.multi_cell(130, 7, 'Analyzes market sentiment and generates trading signals', 1, 'L')

pdf.cell(60, 7, 'Fundamentals Agent', 1, 0, 'L')
pdf.multi_cell(130, 7, 'Analyzes fundamental data and generates trading signals', 1, 'L')

pdf.cell(60, 7, 'Technicals Agent', 1, 0, 'L')
pdf.multi_cell(130, 7, 'Analyzes technical indicators and generates trading signals', 1, 'L')

pdf.cell(60, 7, 'Risk Manager', 1, 0, 'L')
pdf.multi_cell(130, 7, 'Calculates risk metrics and sets position limits', 1, 'L')

pdf.cell(60, 7, 'Portfolio Manager', 1, 0, 'L')
pdf.multi_cell(130, 7, 'Makes final trading decisions and generates orders', 1, 'L')

pdf.ln(10)

# Methodology
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, 'Methodology', 0, 1, 'L')
pdf.set_font('Arial', '', 10)
pdf.multi_cell(0, 5, 'The AI Hedge Fund employs a multi-agent system where each agent analyzes the stocks from a different perspective. These analyses are then consolidated by the Risk Management and Portfolio Management agents to produce final trading decisions.\n\nEach agent brings a unique investment philosophy and analytical approach to the table. Value investors like Ben Graham and Warren Buffett focus on intrinsic value and margin of safety, while growth investors like Cathie Wood and Phil Fisher emphasize innovation and future potential. Specialized agents analyze technical patterns, sentiment indicators, and fundamental metrics to provide a comprehensive view of each security.\n\nThe Risk Management agent evaluates the risk profile of each recommendation, while the Portfolio Management agent makes the final trading decisions based on the collective wisdom of all agents, balancing risk and potential return.')
pdf.ln(5)

# Disclaimer
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, 'Disclaimer', 0, 1, 'L')
pdf.set_font('Arial', '', 10)
pdf.set_fill_color(255, 248, 225)
pdf.multi_cell(0, 5, 'This report is generated for educational purposes only and does not constitute financial advice. All trading decisions should be made in consultation with qualified financial advisors. Past performance is not indicative of future results.\n\nThe AI Hedge Fund is a proof of concept and is not intended for real trading or investment. The system simulates trading decisions but does not actually trade. The creator assumes no liability for financial losses that may result from following the recommendations in this report.', 1, 'L', True)

# Save the PDF
pdf_path = 'ai_hedge_fund_full_report.pdf'
pdf.output(pdf_path)
print(f"PDF successfully created at: {os.path.abspath(pdf_path)}")
