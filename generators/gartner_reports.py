#!/usr/bin/env python3
"""
Gartner-Style Report Generator

Creates analyst-level deep analysis reports similar to Gartner research.
Designed for executives and practitioners who want strategic technical analysis
without fluff or marketing language.

Uses LLM to synthesize and analyze the collected research items.

Gartner-style reports are:
- Analyst-level: Strategic insight for decision makers
- Technically deep: Based on methodology and evidence
- No fluff: No marketing language, no hype, no filler
- Coherent: Synthesizes across sources into strategic narrative
"""

import json
import os
import logging
import re
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class GartnerReportGenerator:
    """
    Generates Gartner-style deep analysis reports.
    
    These reports are:
    - Analyst-level: Strategic insight for decision makers
    - Technically deep: Based on methodology and evidence
    - No fluff: No marketing language, no hype, no filler
    - Coherent: Synthesizes across sources into strategic narrative
    """
    
    def __init__(self, web_dir: str, llm_client=None):
        """
        Initialize the Gartner report generator.
        
        Args:
            web_dir: Base web output directory
            llm_client: Optional LLM client for deep analysis
        """
        self.web_dir = web_dir
        self.data_dir = os.path.join(web_dir, 'data')
        self.llm_client = llm_client
        
    def generate_gartner_report(
        self, 
        date: str, 
        topics: List[str] = None,
        use_llm: bool = True
    ) -> Dict[str, Any]:
        """
        Generate Gartner-style reports for specified topics.
        
        Args:
            date: Date string in YYYY-MM-DD format
            topics: List of topics to analyze (default: vibe_coding, humanoid_robot, physical_ai)
            use_llm: Whether to use LLM for deep analysis
            
        Returns:
            Dict with generation results
        """
        if topics is None:
            topics = ['vibe_coding', 'humanoid_robot', 'physical_ai']
            
        logger.info(f"Generating Gartner reports for {date}")
        
        date_dir = os.path.join(self.data_dir, date)
        reports_dir = os.path.join(date_dir, 'reports')
        
        if not os.path.exists(reports_dir):
            logger.warning(f"No reports directory for {date}")
            return {'generated': [], 'errors': ['No reports directory']}
        
        generated = []
        
        for topic in topics:
            try:
                # Load the MD source file - handle both naming conventions
                topic_filename = topic.replace('_', '-')
                md_file = os.path.join(reports_dir, f'{topic_filename}.md')
                if not os.path.exists(md_file):
                    # Try original name
                    md_file = os.path.join(reports_dir, f'{topic}.md')
                if not os.path.exists(md_file):
                    logger.warning(f"No MD file for {topic}")
                    continue
                    
                with open(md_file, 'r', encoding='utf-8') as f:
                    source_content = f.read()
                
                # Parse items from MD
                items = self._parse_md_items(source_content)
                
                if not items:
                    logger.warning(f"No items parsed for {topic}")
                    continue
                
                logger.info(f"  Parsed {len(items)} items for {topic}")
                
                # Generate deep analysis
                if use_llm and self.llm_client:
                    analysis = self._generate_llm_analysis(topic, items, date)
                else:
                    analysis = self._generate_rulebased_analysis(topic, items, date)
                
                # Save the Gartner report
                topic_name = topic.replace('_', '-')
                output_md = os.path.join(reports_dir, f'gartner-{topic_name}.md')
                output_html = os.path.join(reports_dir, f'gartner-{topic_name}.html')
                
                with open(output_md, 'w', encoding='utf-8') as f:
                    f.write(analysis['markdown'])
                    
                with open(output_html, 'w', encoding='utf-8') as f:
                    f.write(self._markdown_to_html(analysis['markdown']))
                
                generated.append(topic)
                logger.info(f"  Generated Gartner report for {topic}")
                
            except Exception as e:
                logger.error(f"Failed to generate Gartner report for {topic}: {e}")
        
        # Generate index
        self._generate_gartner_index(date, generated, reports_dir)
        
        return {
            'generated': generated,
            'topics': topics
        }
    
    def _parse_md_items(self, md_content: str) -> List[Dict[str, Any]]:
        """
        Parse research items from markdown content.
        
        Extracts title, URL, summary, source for each item.
        """
        items = []
        
        # Split by ## (each item is a section)
        sections = re.split(r'^##\s+', md_content, flags=re.MULTILINE)
        
        for section in sections[1:]:  # Skip first (title/intro)
            lines = section.strip().split('\n')
            if not lines:
                continue
            
            # First line is title (may have number prefix)
            title_match = re.match(r'^\d+\.\s+(.+)$', lines[0].strip())
            if title_match:
                title = title_match.group(1).strip()
            else:
                title = lines[0].strip()
            
            # Find URL
            url = ''
            summary = ''
            source = ''
            
            for i, line in enumerate(lines[1:], 1):
                # URL line
                url_match = re.search(r'\[Read more\]\(([^)]+)\)', line)
                if url_match:
                    url = url_match.group(1)
                
                # Check for summary (non-meta lines)
                if not line.startswith('**Source:') and not line.startswith('---'):
                    if line.strip() and not line.startswith('🔗'):
                        summary += line.strip() + ' '
            
            # Parse source from meta line
            for line in lines:
                if line.startswith('**Source:'):
                    source_match = re.search(r'\*\*Source:\*\*\s+([^|]+)', line)
                    if source_match:
                        source = source_match.group(1).strip()
            
            if title:
                items.append({
                    'title': title,
                    'url': url,
                    'summary': summary.strip(),
                    'source': source
                })
        
        return items
    
    def _generate_llm_analysis(self, topic: str, items: List[Dict], date: str) -> Dict:
        """
        Generate deep analysis using LLM.
        
        Creates Gartner-style synthesis with strategic depth.
        """
        topic_titles = {
            'vibe_coding': 'AI Developer Tools & Vibe Coding',
            'humanoid_robot': 'Humanoid Robotics',
            'physical_ai': 'Physical AI & Embodied Intelligence'
        }
        
        topic_description = {
            'vibe_coding': 'Strategic analysis of AI-powered coding assistants, developer tools, and program synthesis market.',
            'humanoid_robot': 'Market and technical analysis of humanoid robot systems, commercialization, and deployment.',
            'physical_ai': 'Strategic assessment of embodied AI, real-world agent deployment, and industrial applications.'
        }
        
        title = topic_titles.get(topic, topic)
        description = topic_description.get(topic, '')
        
        # Build items context for LLM
        items_context = []
        for i, item in enumerate(items, 1):
            items_context.append(f"""
### Item {i}: {item['title']}
Source: {item['source']}
URL: {item['url']}
Summary: {item['summary']}
""")
        
        items_text = "\n".join(items_context)
        
        # LLM prompt for Gartner-style report
        prompt = f"""You are writing a Gartner-style strategic analysis report on {title}.

CONTEXT:
{description}

Date: {date}

SOURCE MATERIALS:
{items_text}

TASK:
Write a coherent, strategically deep analysis report in the style of Gartner research. This is NOT a summary or list - it's a synthesis that:

1. Provides strategic context and market significance
2. Analyzes technological approaches and their practical implications
3. Evaluates maturity, readiness, and adoption trajectories
4. Identifies key vendors, players, and competitive dynamics
5. Assesses risks, limitations, and open problems
6. Provides actionable guidance for decision makers

REQUIREMENTS:
- Write in analytical prose, not bullet points
- Assume executive/analyst audience - focus on strategic implications
- Be objective and evidence-based
- No marketing language, no fluff, no hype
- Use precise technical terminology where relevant
- Reference specific methods, metrics, and evidence
- Include source references inline

STRUCTURE:
1. Strategic Context (market landscape and significance)
2. Key Developments (analyze what's happening and why it matters)
3. Technology Assessment (methodologies, maturity, tradeoffs)
4. Competitive Landscape (vendors, players, positioning)
5. Risk Factors and Limitations (candid assessment)
6. Strategic Recommendations (what should organizations do)
7. Source References

Write the complete report now:
"""
        
        try:
            # Call LLM - this is a placeholder, actual implementation depends on your LLM client
            if hasattr(self.llm_client, 'call'):
                response = self.llm_client.call(prompt)
                analysis_text = response.content
            else:
                # Fallback if no LLM client
                analysis_text = self._generate_rulebased_analysis(topic, items, date)['markdown']
                
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            analysis_text = self._generate_rulebased_analysis(topic, items, date)['markdown']
        
        return {
            'markdown': analysis_text,
            'topic': topic,
            'date': date,
            'item_count': len(items)
        }
    
    def _generate_rulebased_analysis(self, topic: str, items: List[Dict], date: str) -> Dict:
        """
        Generate analysis without LLM - rule-based synthesis.
        
        Groups items by theme and creates structured technical narrative.
        """
        topic_titles = {
            'vibe_coding': 'AI Developer Tools & Vibe Coding',
            'humanoid_robot': 'Humanoid Robotics', 
            'physical_ai': 'Physical AI & Embodied Intelligence'
        }
        
        title = topic_titles.get(topic, topic)
        
        # Try to group items by inferred themes
        themes = self._infer_themes(items)
        
        lines = [
            f"# {title}",
            f"*Gartner-Style Strategic Analysis | {date}*",
            "",
            f"*This report analyzes {len(items)} sources to provide strategic guidance.*",
            "",
            "---",
            ""
        ]
        
        # Strategic Context
        lines.extend([
            "## Strategic Context",
            "",
            f"Analysis of {len(items)} sources reveals significant developments in {topic.replace('_', ' ')}.",
            "",
        ])
        
        # Add theme-based analysis
        for theme_name, theme_items in themes.items():
            lines.extend([
                f"### {theme_name}",
                "",
            ])
            
            for item in theme_items[:5]:  # Top 5 per theme
                lines.append(f"**{item['title']}**")
                if item['source']:
                    lines.append(f"*{item['source']}*")
                if item['summary']:
                    # Clean and truncate summary
                    summary = item['summary'][:200].strip()
                    if len(item['summary']) > 200:
                        summary += "..."
                    lines.append(summary)
                if item['url']:
                    lines.append(f"[Source]({item['url']})")
                lines.append("")
        
        # Risk Factors
        lines.extend([
            "## Risk Factors and Limitations",
            "",
            "Key considerations:",
            "",
            f"- {len(items)} items analyzed from multiple source types",
            f"- Themes identified: {', '.join(list(themes.keys())[:5])}",
            "- Evidence-based assessment requires review of primary sources",
            "",
        ])
        
        # Strategic Recommendations
        lines.extend([
            "## Strategic Recommendations",
            "",
            "Organizations should:",
            "",
            "- Monitor developments in this space closely",
            "- Evaluate use cases relevant to their domain",
            "- Assess vendor offerings and maturity",
            "- Consider pilot programs for early adoption",
            "",
        ])
        
        # References
        lines.extend([
            "## Source References",
            "",
        ])
        
        for i, item in enumerate(items[:20], 1):  # Top 20 references
            if item['url']:
                lines.append(f"{i}. [{item['title']}]({item['url']})")
            else:
                lines.append(f"{i}. {item['title']}")
        
        return {
            'markdown': '\n'.join(lines),
            'topic': topic,
            'date': date,
            'item_count': len(items)
        }
    
    def _infer_themes(self, items: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Infer themes from items based on keywords.
        
        Simple rule-based clustering.
        """
        theme_keywords = {
            'Language Models & Architecture': ['gpt', 'claude', 'gemini', 'llm', 'model', 'parameter', 'architecture', 'transformer'],
            'Code Generation & Synthesis': ['code', 'generator', 'synthes', 'program', 'cursor', 'windsurf', 'devin'],
            'Robotics & Control': ['robot', 'control', 'locomotion', 'manipulation', 'actuation', 'motor'],
            'Learning & Training': ['train', 'learn', 'gradient', 'optimization', 'fine-tune', 'data'],
            'Perception & Vision': ['vision', 'perception', 'camera', 'sensor', 'visual', 'image'],
            'Safety & Alignment': ['safety', 'align', 'risk', 'security', 'evaluate'],
            'Hardware & Infrastructure': ['chip', 'gpu', 'hardware', 'inference', 'compute', 'nvidia'],
            'Deployment & Systems': ['deploy', 'system', 'production', 'scale', 'serving']
        }
        
        themes = {name: [] for name in theme_keywords}
        themes['Other'] = []
        
        for item in items:
            text = f"{item.get('title', '')} {item.get('summary', '')}".lower()
            
            assigned = False
            for theme_name, keywords in theme_keywords.items():
                if theme_name == 'Other':
                    continue
                for kw in keywords:
                    if kw in text:
                        themes[theme_name].append(item)
                        assigned = True
                        break
                if assigned:
                    break
            
            if not assigned:
                themes['Other'].append(item)
        
        # Remove empty themes and sort by count
        themes = {k: v for k, v in themes.items() if v}
        themes = dict(sorted(themes.items(), key=lambda x: len(x[1]), reverse=True))
        
        return themes
    
    def _markdown_to_html(self, md: str) -> str:
        """Convert markdown to HTML."""
        import re
        
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gartner-Style Strategic Analysis</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.7;
            color: #1a1a1a;
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        h1 {
            font-size: 1.8em;
            margin-bottom: 10px;
            color: #1a1a1a;
            border-bottom: 3px solid #0066cc;
            padding-bottom: 15px;
        }
        h2 {
            font-size: 1.3em;
            margin-top: 35px;
            margin-bottom: 15px;
            color: #1a1a1a;
            border-bottom: 1px solid #e0e0e0;
            padding-bottom: 8px;
        }
        h3 {
            font-size: 1.1em;
            margin-top: 25px;
            margin-bottom: 10px;
            color: #333;
        }
        p {
            margin-bottom: 15px;
        }
        a {
            color: #0066cc;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        .meta {
            color: #666;
            font-size: 0.9em;
            margin-bottom: 20px;
        }
        ul, ol {
            margin-bottom: 15px;
            padding-left: 25px;
        }
        li {
            margin-bottom: 8px;
        }
        blockquote {
            border-left: 4px solid #0066cc;
            margin: 20px 0;
            padding: 15px 20px;
            background: #f8f9fa;
            color: #444;
        }
        hr {
            border: none;
            border-top: 1px solid #ddd;
            margin: 30px 0;
        }
        .nav {
            margin-bottom: 30px;
        }
        .nav a {
            margin-right: 15px;
            color: #0066cc;
            font-weight: 500;
        }
        .badge {
            display: inline-block;
            background: #0066cc;
            color: white;
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="nav">
            <a href="index.html">← All Reports</a>
            <a href="gartner-vibe-coding.html">Vibe Coding</a>
            <a href="gartner-humanoid-robot.html">Humanoid Robots</a>
            <a href="gartner-physical-ai.html">Physical AI</a>
        </div>
"""
        
        # Convert markdown to HTML
        lines = md.split('\n')
        in_list = False
        
        for line in lines:
            # Headers
            if line.startswith('# '):
                html += f'<h1>{line[2:]}</h1>\n'
            elif line.startswith('## '):
                html += f'<h2>{line[3:]}</h2>\n'
            elif line.startswith('### '):
                html += f'<h3>{line[4:]}</h3>\n'
            # Horizontal rule
            elif line == '---':
                html += '<hr>\n'
            # Bold
            line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
            # Italic
            line = re.sub(r'\*(.+?)\*', r'<em>\1</em>', line)
            # Links
            line = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', line)
            # List items
            if line.startswith('- '):
                if not in_list:
                    html += '<ul>\n'
                    in_list = True
                html += f'<li>{line[2:]}</li>\n'
            else:
                if in_list:
                    html += '</ul>\n'
                    in_list = False
                if line.strip():
                    html += f'<p>{line}</p>\n'
        
        if in_list:
            html += '</ul>\n'
        
        html += """
        <hr>
        <p class="meta">Gartner-Style Strategic Analysis | AI News Aggregator</p>
    </div>
</body>
</html>
"""
        
        return html
    
    def _generate_gartner_index(self, date: str, generated: List[str], reports_dir: str):
        """Generate index page for Gartner reports."""
        
        topic_titles = {
            'vibe_coding': 'AI Developer Tools & Vibe Coding',
            'humanoid_robot': 'Humanoid Robotics',
            'physical_ai': 'Physical AI & Embodied Intelligence'
        }
        
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gartner-Style Strategic Reports</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 8px;
        }
        h1 {
            text-align: center;
            margin-bottom: 10px;
            color: #1a1a1a;
        }
        .date {
            text-align: center;
            color: #666;
            margin-bottom: 40px;
        }
        .reports {
            display: grid;
            gap: 20px;
        }
        .report-card {
            padding: 25px;
            border-radius: 8px;
            border-left: 5px solid #0066cc;
            background: #f8f9fa;
            text-decoration: none;
            color: inherit;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .report-card:hover {
            transform: translateX(5px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        .report-card h2 {
            margin-top: 0;
            font-size: 1.2em;
            color: #0066cc;
            border: none;
        }
        .report-card p {
            color: #555;
            margin: 0;
        }
        .back-link {
            display: block;
            text-align: center;
            margin-top: 40px;
            color: #0066cc;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Gartner-Style Strategic Reports</h1>
    <p class="date">""" + date + """</p>
    
    <p style="text-align:center;margin-bottom:30px;">
        Analyst-level strategic analysis. Evidence-based. No fluff.
    </p>
    
    <div class="reports">
"""
        
        for topic in generated:
            title = topic_titles.get(topic, topic)
            filename = f'gartner-{topic.replace("_", "-")}.html'
            
            html += f"""
        <a href="{filename}" class="report-card">
            <h2>{title}</h2>
            <p>Strategic analysis →</p>
        </a>
"""
        
        html += """
    </div>
    
    <a href="index.html" class="back-link">← Back to Report Index</a>
    </div>
</body>
</html>
"""
        
        index_path = os.path.join(reports_dir, 'gartner-index.html')
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(html)


def generate_gartner_reports(
    web_dir: str, 
    date: str = None,
    llm_client = None,
    topics: List[str] = None
) -> Dict[str, Any]:
    """
    Convenience function to generate Gartner-style reports.
    
    Args:
        web_dir: Web output directory
        date: Date string (YYYY-MM-DD). If None, uses most recent.
        llm_client: Optional LLM client for deep analysis
        topics: Topics to generate reports for
        
    Returns:
        Dict with generation results
    """
    if date is None:
        data_dir = os.path.join(web_dir, 'data')
        if not os.path.exists(data_dir):
            return {'error': 'No data directory'}
        
        dates = [d for d in os.listdir(data_dir) 
                 if os.path.isdir(os.path.join(data_dir, d)) 
                 and d.startswith('202')]
        
        if not dates:
            return {'error': 'No date directories'}
        
        date = max(dates)
    
    generator = GartnerReportGenerator(web_dir, llm_client=llm_client)
    return generator.generate_gartner_report(date, topics=topics)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python gartner_reports.py <web_dir> [date]")
        sys.exit(1)
    
    web_dir = sys.argv[1]
    date = sys.argv[2] if len(sys.argv) > 2 else None
    
    logging.basicConfig(level=logging.INFO)
    
    result = generate_gartner_reports(web_dir, date)
    print(f"\nGenerated Gartner reports: {result}")
