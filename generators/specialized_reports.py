#!/usr/bin/env python3
"""
Specialized Report Generator

Generates focused reports for specific topics:
- Vibe Coding: AI coding assistants, developer tools, code generation
- Humanoid Robots & Physical AI: Robotics, embodied AI, automation

Outputs:
- HTML and Markdown formats
- Located in web/data/{date}/reports/ directory
"""

import json
import os
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

# Topic keywords for filtering
VIBE_CODING_KEYWORDS = [
    'cursor', 'windsurf', 'v0', 'bolt.new', 'bolt.new', 'github copilot',
    'code generation', 'ai coding', 'code assistant', 'developer tool',
    'vibe coding', 'pair programming', 'code completion', 'refactor',
    'cursor IDE', 'lovable', 'replit', ' Lovable', 'codeium', 'tabnine',
    'sourcegraph', 'code intelligence', 'ai developer', 'devin', 
    'swe-agent', 'software engineering', 'program synthesis'
]

HUMANOID_ROBOT_KEYWORDS = [
    'humanoid', 'atlas', 'tesla optimus', 'optimus', 'figure ai', 
    'agility robotics', 'digit robot', 'boston dynamics', 'robotics',
    'physical ai', 'embodied ai', 'robot arm', 'manipulation', 
    'locomotion', 'walking robot', 'humanoid robot', 'android',
    ' bipedal', 'dexterity', 'grasping', 'robot learning', 'real-world ai',
    'factory robot', 'warehouse robot', 'automation', 'robot deployment',
    'tesla robot', 'apptronik', ' Sanctuary AI', 'cyberdyne',
    'robot control', 'sim2real', 'foundation for robot'
]

PHYSICAL_AI_KEYWORDS = [
    'physical ai', 'embodied intelligence', 'robotics', 'automation',
    'smart factory', 'industrial robot', 'manufacturing ai', 
    'perception-action', 'sensorimotor', 'real world ai', 'grounded ai',
    'agent deployment', 'world model', 'sim2real', 'transfer learning robot',
    'learning to walk', 'motion planning', 'control policy'
]


def classify_item(title: str, content: str, summary: str = '', tags: List[str] = None) -> List[str]:
    """
    Classify an item into topic categories based on keywords.
    
    Returns list of matching topics: ['vibe_coding', 'humanoid_robot', 'physical_ai']
    """
    text = f"{title} {content} {summary}".lower()
    if tags:
        text += " " + " ".join(tags).lower()
    
    topics = []
    
    # Check vibe coding
    for keyword in VIBE_CODING_KEYWORDS:
        if keyword.lower() in text:
            topics.append('vibe_coding')
            break
    
    # Check humanoid robot
    for keyword in HUMANOID_ROBOT_KEYWORDS:
        if keyword.lower() in text:
            topics.append('humanoid_robot')
            break
    
    # Check physical AI
    for keyword in PHYSICAL_AI_KEYWORDS:
        if keyword.lower() in text:
            topics.append('physical_ai')
            break
    
    return list(set(topics))  # Remove duplicates


def markdown_to_html(text: str) -> str:
    """Convert basic markdown to HTML."""
    if not text:
        return ''
    
    import re
    
    # Convert headers
    text = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', text, flags=re.MULTILINE)
    text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    
    # Convert bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    
    # Convert links
    def link_replacer(match):
        link_text, url = match.groups()
        if url.startswith('/') or url.startswith('#'):
            return f'<a href="{url}" class="internal-link">{link_text}</a>'
        else:
            return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{link_text}</a>'
    
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link_replacer, text)
    
    # Convert bullet lists
    lines = text.split('\n')
    in_list = False
    result = []
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('- '):
            if not in_list:
                result.append('<ul>')
                in_list = True
            bullet_content = stripped[2:]
            result.append(f'<li>{bullet_content}</li>')
        else:
            if in_list:
                result.append('</ul>')
                in_list = False
            if stripped:
                if stripped.startswith(('<h2>', '<h3>', '<h4>', '<ul>')):
                    result.append(stripped)
                else:
                    result.append(f'<p>{stripped}</p>')
    
    if in_list:
        result.append('</ul>')
    
    return '\n'.join(result)


class SpecializedReportGenerator:
    """Generates focused reports for specific topics."""
    
    def __init__(self, web_dir: str):
        """
        Initialize the generator.
        
        Args:
            web_dir: Base web output directory
        """
        self.web_dir = web_dir
        self.data_dir = os.path.join(web_dir, 'data')
        
    def generate_reports(self, date: str) -> Dict[str, Any]:
        """
        Generate specialized reports for a given date.
        
        Args:
            date: Date string in YYYY-MM-DD format
            
        Returns:
            Dict with generation results
        """
        logger.info(f"Generating specialized reports for {date}")
        
        # Load the category data
        date_dir = os.path.join(self.data_dir, date)
        if not os.path.exists(date_dir):
            logger.warning(f"No data directory for {date}")
            return {'generated': [], 'errors': ['No data directory']}
        
        # Load all categories
        all_items = []
        
        for category in ['news', 'research', 'social', 'reddit']:
            category_path = os.path.join(date_dir, f'{category}.json')
            if os.path.exists(category_path):
                with open(category_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    items = data.get('items', [])
                    for item in items:
                        item['category'] = category
                    all_items.extend(items)
        
        logger.info(f"Loaded {len(all_items)} total items")
        
        # Classify items by topic
        vibe_coding_items = []
        humanoid_robot_items = []
        physical_ai_items = []
        
        for item in all_items:
            topics = classify_item(
                item.get('title', ''),
                item.get('content', ''),
                item.get('summary', ''),
                item.get('tags', [])
            )
            
            if 'vibe_coding' in topics:
                vibe_coding_items.append(item)
            if 'humanoid_robot' in topics:
                humanoid_robot_items.append(item)
            if 'physical_ai' in topics:
                physical_ai_items.append(item)
        
        logger.info(f"Classified items: vibe_coding={len(vibe_coding_items)}, "
                   f"humanoid_robot={len(humanoid_robot_items)}, physical_ai={len(physical_ai_items)}")
        
        # Create reports directory
        reports_dir = os.path.join(date_dir, 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        
        generated = []
        
        # Generate Vibe Coding report
        if vibe_coding_items:
            try:
                self._generate_report(
                    date=date,
                    topic='vibe_coding',
                    title='Vibe Coding',
                    description='AI coding assistants, developer tools, and code generation news',
                    items=vibe_coding_items,
                    output_dir=reports_dir
                )
                generated.append('vibe_coding')
            except Exception as e:
                logger.error(f"Failed to generate vibe coding report: {e}")
        
        # Generate Humanoid Robot report
        if humanoid_robot_items:
            try:
                self._generate_report(
                    date=date,
                    topic='humanoid_robot',
                    title='Humanoid Robots',
                    description='Humanoid robot news, videos, and developments',
                    items=humanoid_robot_items,
                    output_dir=reports_dir
                )
                generated.append('humanoid_robot')
            except Exception as e:
                logger.error(f"Failed to generate humanoid robot report: {e}")
        
        # Generate Physical AI report
        if physical_ai_items:
            try:
                self._generate_report(
                    date=date,
                    topic='physical_ai',
                    title='Physical AI',
                    description='Embodied AI, robotics, automation, and real-world AI deployment',
                    items=physical_ai_items,
                    output_dir=reports_dir
                )
                generated.append('physical_ai')
            except Exception as e:
                logger.error(f"Failed to generate physical AI report: {e}")
        
        # Also generate combined Humanoid + Physical AI report
        combined_items = humanoid_robot_items + physical_ai_items
        if combined_items:
            # Remove duplicates based on URL
            seen_urls = set()
            unique_items = []
            for item in combined_items:
                url = item.get('url', '')
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    unique_items.append(item)
            
            try:
                self._generate_report(
                    date=date,
                    topic='robots_physical_ai',
                    title='Humanoid Robots & Physical AI',
                    description='Combined report on humanoid robots and physical AI developments',
                    items=unique_items,
                    output_dir=reports_dir,
                    combined=True
                )
                generated.append('robots_physical_ai')
            except Exception as e:
                logger.error(f"Failed to generate combined robots report: {e}")
        
        # Generate index of all reports
        self._generate_report_index(date, generated, reports_dir)
        
        logger.info(f"Generated {len(generated)} specialized reports")
        
        return {
            'generated': generated,
            'counts': {
                'vibe_coding': len(vibe_coding_items),
                'humanoid_robot': len(humanoid_robot_items),
                'physical_ai': len(physical_ai_items),
                'robots_physical_ai': len(unique_items) if combined_items else 0
            }
        }
    
    def _generate_report(
        self,
        date: str,
        topic: str,
        title: str,
        description: str,
        items: List[Dict],
        output_dir: str,
        combined: bool = False
    ):
        """Generate HTML and Markdown reports for a topic."""
        
        # Sort by importance score
        items_sorted = sorted(
            items, 
            key=lambda x: x.get('importance_score', 0), 
            reverse=True
        )
        
        # Build markdown content
        md_content = self._build_markdown(
            date, title, description, items_sorted, combined
        )
        
        # Build HTML content
        html_content = self._build_html(
            date, title, description, items_sorted, combined
        )
        
        # Write files
        if combined:
            base_name = 'robots-physical-ai'
        else:
            base_name = topic.replace('_', '-')
        
        md_path = os.path.join(output_dir, f'{base_name}.md')
        html_path = os.path.join(output_dir, f'{base_name}.html')
        
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"  Generated: {base_name}.md ({len(items_sorted)} items)")
        logger.info(f"  Generated: {base_name}.html ({len(items_sorted)} items)")
    
    def _build_markdown(
        self,
        date: str,
        title: str,
        description: str,
        items: List[Dict],
        combined: bool
    ) -> str:
        """Build Markdown content for a report."""
        
        from datetime import datetime
        
        # Format date nicely
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            date_formatted = date_obj.strftime('%B %d, %Y')
        except:
            date_formatted = date
        
        lines = [
            f"# {title}",
            "",
            f"**Date:** {date_formatted}",
            "",
            f"*{description}*",
            "",
            f"*This report contains {len(items)} curated items*",
            "",
            "---",
            ""
        ]
        
        # Add items
        for i, item in enumerate(items, 1):
            item_title = item.get('title', 'Untitled')
            item_url = item.get('url', '')
            item_summary = item.get('summary', item.get('content', ''))
            item_source = item.get('source', 'Unknown')
            item_category = item.get('category', 'news')
            item_score = item.get('importance_score', 0)
            
            lines.append(f"## {i}. {item_title}")
            lines.append("")
            
            if item_url:
                lines.append(f"🔗 [Read more]({item_url})")
                lines.append("")
            
            if item_summary:
                # Truncate long summaries
                if len(item_summary) > 300:
                    item_summary = item_summary[:300] + "..."
                lines.append(item_summary)
                lines.append("")
            
            lines.append(f"**Source:** {item_source} | **Category:** {item_category} | **Score:** {item_score}/100")
            lines.append("")
            lines.append("---")
            lines.append("")
        
        # Add footer
        lines.extend([
            "",
            "---",
            "",
            f"*Generated by AI News Aggregator on {date_formatted}*",
            "",
            "**Other Reports:**",
            "- [Main Summary](/?date={date})".format(date=date),
            "- [Vibe Coding](./vibe-coding.md)",
            "- [Humanoid Robots](./humanoid-robot.md)",
            "- [Physical AI](./physical-ai.md)",
            "- [Robots & Physical AI](./robots-physical-ai.md)"
        ])
        
        return '\n'.join(lines)
    
    def _build_html(
        self,
        date: str,
        title: str,
        description: str,
        items: List[Dict],
        combined: bool
    ) -> str:
        """Build HTML content for a report."""
        
        from datetime import datetime
        
        # Format date nicely
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            date_formatted = date_obj.strftime('%B %d, %Y')
        except:
            date_formatted = date
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - AI News Aggregator</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        h1 {{ font-size: 2em; margin-bottom: 10px; }}
        .subtitle {{ opacity: 0.9; font-size: 1.1em; }}
        .meta {{
            display: flex;
            gap: 20px;
            margin-top: 15px;
            font-size: 0.9em;
            opacity: 0.9;
        }}
        .item {{
            background: white;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .item h2 {{
            font-size: 1.2em;
            margin-bottom: 10px;
            color: #1a1a1a;
        }}
        .item h2 a {{
            color: #667eea;
            text-decoration: none;
        }}
        .item h2 a:hover {{
            text-decoration: underline;
        }}
        .item-summary {{
            color: #555;
            margin: 10px 0;
        }}
        .item-meta {{
            display: flex;
            gap: 15px;
            font-size: 0.85em;
            color: #777;
            margin-top: 10px;
        }}
        .category {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            text-transform: uppercase;
        }}
        .category.news {{ background: #e3f2fd; color: #1565c0; }}
        .category.research {{ background: #e8f5e9; color: #2e7d32; }}
        .category.social {{ background: #fff3e0; color: #e65100; }}
        .category.reddit {{ background: #fce4ec; color: #c2185b; }}
        .score {{
            font-weight: bold;
            color: #667eea;
        }}
        footer {{
            text-align: center;
            padding: 20px;
            color: #777;
            font-size: 0.9em;
        }}
        .nav-links {{
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            justify-content: center;
            margin-top: 10px;
        }}
        .nav-links a {{
            color: white;
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <header>
        <h1>{title}</h1>
        <p class="subtitle">{description}</p>
        <div class="meta">
            <span>📅 {date_formatted}</span>
            <span>📊 {len(items)} curated items</span>
        </div>
        <div class="nav-links">
            <a href="../index.html">← Main Summary</a>
            <a href="./vibe-coding.html">Vibe Coding</a>
            <a href="./humanoid-robot.html">Humanoid Robots</a>
            <a href="./physical-ai.html">Physical AI</a>
        </div>
    </header>
    
    <main>
"""
        
        # Add items
        for i, item in enumerate(items, 1):
            item_title = item.get('title', 'Untitled')
            item_url = item.get('url', '')
            item_summary = item.get('summary', item.get('content', ''))
            item_source = item.get('source', 'Unknown')
            item_category = item.get('category', 'news')
            item_score = item.get('importance_score', 0)
            
            # Truncate long summaries
            if len(item_summary) > 400:
                item_summary = item_summary[:400] + "..."
            
            title_html = f'<a href="{item_url}" target="_blank" rel="noopener">{item_title}</a>' if item_url else item_title
            
            html += f"""
        <article class="item">
            <h2>{i}. {title_html}</h2>
            <p class="item-summary">{item_summary}</p>
            <div class="item-meta">
                <span>📰 {item_source}</span>
                <span class="category {item_category}">{item_category}</span>
                <span class="score">⭐ {item_score}/100</span>
            </div>
        </article>
"""
        
        html += f"""
    </main>
    
    <footer>
        <p>Generated by AI News Aggregator</p>
        <p>{date_formatted}</p>
    </footer>
</body>
</html>
"""
        
        return html
    
    def _generate_report_index(self, date: str, generated: List[str], reports_dir: str):
        """Generate an index page for all reports."""
        
        from datetime import datetime
        
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            date_formatted = date_obj.strftime('%B %d, %Y')
        except:
            date_formatted = date
        
        report_titles = {
            'vibe_coding': ('Vibe Coding', 'AI coding assistants and developer tools'),
            'humanoid_robot': ('Humanoid Robots', 'Humanoid robot news and developments'),
            'physical_ai': ('Physical AI', 'Embodied AI and robotics'),
            'robots_physical_ai': ('Robots & Physical AI', 'Combined humanoid robots and physical AI report')
        }
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Specialized Reports - AI News Aggregator</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
            background: #f5f5f5;
        }}
        h1 {{
            text-align: center;
            margin-bottom: 10px;
            color: #1a1a1a;
        }}
        .date {{
            text-align: center;
            color: #666;
            margin-bottom: 40px;
        }}
        .reports {{
            display: grid;
            gap: 20px;
        }}
        .report-card {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            text-decoration: none;
            color: inherit;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .report-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        .report-card h2 {{
            color: #667eea;
            margin-bottom: 8px;
        }}
        .report-card p {{
            color: #555;
            margin: 0;
        }}
        .back-link {{
            display: block;
            text-align: center;
            margin-top: 40px;
            color: #667eea;
            text-decoration: none;
        }}
        .back-link:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <h1>📋 Specialized Reports</h1>
    <p class="date">{date_formatted}</p>
    
    <div class="reports">
"""
        
        for topic in generated:
            if topic in report_titles:
                title, desc = report_titles[topic]
                filename = topic.replace('_', '-')
                if topic == 'robots_physical_ai':
                    filename = 'robots-physical-ai'
                
                html += f"""
        <a href="{filename}.html" class="report-card">
            <h2>{title}</h2>
            <p>{desc}</p>
        </a>
"""
        
        html += """
    </div>
    
    <a href="../index.html" class="back-link">← Back to Main Summary</a>
</body>
</html>
"""
        
        index_path = os.path.join(reports_dir, 'index.html')
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        logger.info(f"  Generated report index: index.html")


def generate_reports_for_date(web_dir: str, date: str = None) -> Dict[str, Any]:
    """
    Convenience function to generate reports for a specific date.
    
    Args:
        web_dir: Web output directory
        date: Date string (YYYY-MM-DD). If None, uses most recent date.
        
    Returns:
        Dict with generation results
    """
    if date is None:
        # Find most recent date with data
        data_dir = os.path.join(web_dir, 'data')
        if not os.path.exists(data_dir):
            return {'error': 'No data directory'}
        
        dates = [d for d in os.listdir(data_dir) 
                 if os.path.isdir(os.path.join(data_dir, d)) 
                 and d.startswith('202')]
        
        if not dates:
            return {'error': 'No date directories found'}
        
        date = max(dates)
    
    generator = SpecializedReportGenerator(web_dir)
    return generator.generate_reports(date)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python specialized_reports.py <web_dir> [date]")
        sys.exit(1)
    
    web_dir = sys.argv[1]
    date = sys.argv[2] if len(sys.argv) > 2 else None
    
    logging.basicConfig(level=logging.INFO)
    
    result = generate_reports_for_date(web_dir, date)
    print(f"\nGenerated reports: {result}")
