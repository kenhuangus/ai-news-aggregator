#!/usr/bin/env python3
"""
Gartner-Style Report Generator - Enhanced Version

Creates analyst-level deep analysis reports similar to Gartner research.
This version includes:
- Enhanced LLM prompts with Gartner frameworks
- Multi-pass analysis pipeline
- Quality scoring system
- Structured data enrichment
- Async LLM client support

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
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

# Quality score thresholds
MIN_QUALITY_SCORE = 60
MAX_GENERATION_ATTEMPTS = 3


class GartnerReportGenerator:
    """
    Generates Gartner-style deep analysis reports with enhanced quality.
    
    These reports are:
    - Analyst-level: Strategic insight for decision makers
    - Technically deep: Based on methodology and evidence
    - No fluff: No marketing language, no hype, no filler
    - Coherent: Synthesizes across sources into strategic narrative
    """
    
    # Gartner framework definitions
    GARTNER_FRAMEWORKS = {
        'maturity_model': {
            'Emerging': 'Technologies in early research/proof-of-concept stage',
            'Trending': 'Growing interest and investment, early commercial deployments',
            'Mature': 'Widely adopted, stable technology with established best practices',
            'Declining': 'Technology reaching end-of-life or being superseded'
        },
        'hype_cycle': {
            'Innovation Trigger': 'Early interest from media and industry',
            'Peak of Inflated Expectations': 'Hype exceeds early success stories',
            'Trough of Disillusionment': 'Reality fails to meet expectations',
            'Slope of Enlightenment': 'Practical use cases emerge',
            'Plateau of Productivity': 'Mainstream adoption begins'
        },
        'business_impact': {
            'Transformational': 'Fundamentally changes industry economics and competition',
            'High': 'Significant impact on business processes and outcomes',
            'Moderate': 'Noticeable improvement to existing processes',
            'Low': 'Limited but positive impact on operations'
        },
        'adoption_timeline': {
            'Immediate': 'Action recommended within 0-3 months',
            'Near-term': 'Evaluate and plan for 3-6 months',
            'Mid-term': 'Monitor and prepare for 6-12 months',
            'Long-term': 'Track developments for 12+ months'
        }
    }
    
    # Fluff words to avoid
    FLUFF_INDICATORS = [
        'game-changer', 'revolutionary', 'breakthrough', 'unprecedented',
        'paradigm shift', 'disruptive', 'game changing', 'amazing',
        'incredible', 'mind-blowing', 'once-in-a-lifetime'
    ]
    
    def __init__(self, web_dir: str, llm_client=None, async_llm_client=None):
        """
        Initialize the Gartner report generator.
        
        Args:
            web_dir: Base web output directory
            llm_client: Optional sync LLM client for deep analysis
            async_llm_client: Optional async LLM client for parallel processing
        """
        self.web_dir = web_dir
        self.data_dir = os.path.join(web_dir, 'data')
        self.llm_client = llm_client
        self.async_llm_client = async_llm_client
        
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
        quality_scores = {}
        
        for topic in topics:
            try:
                # Load the MD source file - handle both naming conventions
                topic_filename = topic.replace('_', '-')
                md_file = os.path.join(reports_dir, f'{topic_filename}.md')
                if not os.path.exists(md_file):
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
                
                # Enrich items with structured data (Strategy 4)
                enriched_items = self._enrich_with_data(items)
                
                # Generate analysis with multi-pass (Strategy 2)
                if use_llm and (self.llm_client or self.async_llm_client):
                    analysis = self._generate_multipass_analysis(topic, enriched_items, date)
                else:
                    analysis = self._generate_rulebased_analysis(topic, enriched_items, date)
                
                # Score quality (Strategy 3)
                quality_score = self._score_report_quality(analysis['markdown'])
                quality_scores[topic] = quality_score
                logger.info(f"  Quality score for {topic}: {quality_score}/100")
                
                # Regenerate if quality too low
                if quality_score < MIN_QUALITY_SCORE:
                    logger.warning(f"  Quality score below threshold ({quality_score} < {MIN_QUALITY_SCORE}), attempting regeneration...")
                    # Could add retry logic here
                
                # Save the Gartner report
                topic_name = topic.replace('_', '-')
                output_md = os.path.join(reports_dir, f'gartner-{topic_name}.md')
                output_html = os.path.join(reports_dir, f'gartner-{topic_name}.html')
                
                with open(output_md, 'w', encoding='utf-8') as f:
                    f.write(analysis['markdown'])
                    
                with open(output_html, 'w', encoding='utf-8') as f:
                    f.write(self._markdown_to_html(analysis['markdown']))
                
                generated.append(topic)
                logger.info(f"  Generated Gartner report for {topic} (quality: {quality_score})")
                
            except Exception as e:
                logger.error(f"Failed to generate Gartner report for {topic}: {e}")
        
        # Generate index
        self._generate_gartner_index(date, generated, reports_dir)
        
        return {
            'generated': generated,
            'topics': topics,
            'quality_scores': quality_scores
        }
    
    # ==================== STRATEGY 4: Structured Data Enrichment ====================
    
    def _enrich_with_data(self, items: List[Dict]) -> List[Dict]:
        """
        Enrich items with structured data extraction.
        
        Extracts metrics, vendors, dates, and other structured info.
        """
        enriched = []
        
        for item in items:
            text = f"{item.get('title', '')} {item.get('summary', '')}"
            
            # Extract metrics (percentages, dollar amounts, ratios)
            metrics = re.findall(
                r'\$[\d,]+(?:\.\d+)?[BMK]?|\d+(?:\.\d+)?%',
                text
            )
            
            # Extract dates
            dates = re.findall(
                r'\b(20\d{2}[-/]\d{1,2}[-/]\d{1,2}|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b)',
                text,
                re.IGNORECASE
            )
            
            # Extract vendor/company names (common AI companies)
            vendors = []
            company_patterns = [
                r'\b(OpenAI|Anthropic|Google|DeepMind|Microsoft|Meta|Stability|Firebase|X|Tesla|Boston Dynamics|Figure|Techtronic|Amazon)\b',
                r'\b(Claude|GPT|Gemini|Llama|Stable Diffusion)\b'
            ]
            for pattern in company_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                vendors.extend([v.capitalize() for v in matches])
            vendors = list(set(vendors))[:5]  # Limit to 5
            
            enriched_item = {
                **item,
                'metrics': metrics[:10],  # Top 10 metrics
                'dates': dates[:5],  # Top 5 dates
                'vendors': vendors
            }
            enriched.append(enriched_item)
        
        return enriched
    
    # ==================== STRATEGY 2: Multi-Pass Analysis Pipeline ====================
    
    def _generate_multipass_analysis(
        self, 
        topic: str, 
        items: List[Dict], 
        date: str
    ) -> Dict:
        """
        Generate analysis using multi-pass approach.
        
        Pass 1: Extract key facts and claims
        Pass 2: Synthesize into strategic themes  
        Pass 3: Apply Gartner frameworks
        Pass 4: Generate final polished report
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
        
        # Build enriched items context
        items_context = self._build_enriched_context(items)
        
        # Use async if available, otherwise sync
        if self.async_llm_client:
            return asyncio.run(self._async_multipass(topic, title, description, items_context, items, date))
        else:
            return self._sync_multipass(topic, title, description, items_context, items, date)
    
    async def _async_multipass(
        self, 
        topic: str, 
        title: str, 
        description: str,
        items_context: str,
        items: List[Dict],
        date: str
    ) -> Dict:
        """Async multi-pass analysis."""
        # Pass 1 & 2 combined: Extract facts and synthesize themes
        pass1_prompt = self._get_fact_extraction_prompt(items_context, title)
        
        try:
            response = await self.async_llm_client.call_with_thinking(
                messages=[{"role": "user", "content": pass1_prompt}],
                budget_tokens=8192,
                caller=f"gartner_{topic}_facts"
            )
            facts_and_themes = response.content
        except Exception as e:
            logger.warning(f"Fact extraction failed: {e}")
            facts_and_themes = items_context
        
        # Pass 3: Apply frameworks and generate final report
        pass3_prompt = self._get_framework_prompt(
            topic=topic,
            title=title,
            description=description,
            facts_and_themes=facts_and_themes,
            items=items,
            date=date
        )
        
        try:
            response = await self.async_llm_client.call_with_thinking(
                messages=[{"role": "user", "content": pass3_prompt}],
                budget_tokens=16000,
                caller=f"gartner_{topic}_final"
            )
            analysis_text = response.content
        except Exception as e:
            logger.error(f"Final generation failed: {e}")
            analysis_text = self._generate_rulebased_analysis(topic, items, date)['markdown']
        
        return {
            'markdown': analysis_text,
            'topic': topic,
            'date': date,
            'item_count': len(items)
        }
    
    def _sync_multipass(
        self, 
        topic: str, 
        title: str, 
        description: str,
        items_context: str,
        items: List[Dict],
        date: str
    ) -> Dict:
        """Sync multi-pass analysis (fallback)."""
        # Pass 1 & 2: Get enhanced prompt with frameworks
        prompt = self._get_enhanced_gartner_prompt(
            topic=topic,
            title=title,
            description=description,
            items_context=items_context,
            date=date
        )
        
        try:
            if hasattr(self.llm_client, 'call'):
                response = self.llm_client.call(prompt)
                analysis_text = response.content
            else:
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
    
    # ==================== STRATEGY 1: Enhanced LLM Prompts ====================
    
    def _build_enriched_context(self, items: List[Dict]) -> str:
        """Build enriched context with metrics and vendors."""
        parts = []
        for i, item in enumerate(items, 1):
            parts.append(f"### Item {i}: {item['title']}")
            parts.append(f"Source: {item.get('source', 'Unknown')}")
            if item.get('vendors'):
                parts.append(f"Companies: {', '.join(item['vendors'])}")
            if item.get('metrics'):
                parts.append(f"Key Numbers: {', '.join(item['metrics'])}")
            parts.append(f"Summary: {item['summary']}")
            if item.get('url'):
                parts.append(f"URL: {item['url']}")
            parts.append("")
        return "\n".join(parts)
    
    def _get_enhanced_gartner_prompt(
        self, 
        topic: str, 
        title: str, 
        description: str,
        items_context: str,
        date: str
    ) -> str:
        """Enhanced prompt with Gartner frameworks and strict requirements."""
        frameworks = self.GARTNER_FRAMEWORKS
        
        return f"""You are a Gartner Senior Analyst writing strategic analysis for Fortune 500 CTOs and technology leaders.

TOPIC: {title}
{description}
Date: {date}

ANALYST FRAMEWORKS TO APPLY:

1. TECHNOLOGY MATURITY ASSESSMENT:
   - Emerging: {frameworks['maturity_model']['Emerging']}
   - Trending: {frameworks['maturity_model']['Trending']}
   - Mature: {frameworks['maturity_model']['Mature']}
   - Declining: {frameworks['maturity_model']['Declining']}

2. BUSINESS IMPACT RATING:
   - Transformational: {frameworks['business_impact']['Transformational']}
   - High: {frameworks['business_impact']['High']}
   - Moderate: {frameworks['business_impact']['Moderate']}
   - Low: {frameworks['business_impact']['Low']}

3. ADOPTION TIMELINE:
   - Immediate: {frameworks['adoption_timeline']['Immediate']}
   - Near-term: {frameworks['adoption_timeline']['Near-term']}
   - Mid-term: {frameworks['adoption_timeline']['Mid-term']}
   - Long-term: {frameworks['adoption_timeline']['Long-term']}

SOURCE MATERIALS:
{items_context}

STRICT REQUIREMENTS - WRITE LIKE A GARTNER ANALYST:

1. WRITING STYLE:
   - Write in analytical PROSE, NOT bullet points
   - Every paragraph should be 3-5 sentences with analytical depth
   - No marketing language, no hype, no fluff
   - Use precise technical terminology
   - Be objective and evidence-based

2. STRUCTURE (Follow exactly):
   ## Strategic Context
   - Market landscape and significance
   - Why this matters to enterprise technology leaders
   
   ## Key Developments  
   - What's happening and why it matters
   - Connect to broader industry trends
   
   ## Technology Assessment
   - Apply Maturity Model to each major technology
   - Evaluate methodologies, tradeoffs, readiness
   
   ## Competitive Landscape
   - Key vendors, players, market positioning
   - Vendor-agnostic assessment
   
   ## Risk Factors and Limitations
   - Candid assessment of challenges
   - What could go wrong
   
   ## Strategic Recommendations
   - What should organizations do?
   - Use adoption timeline framework
   - Prioritize by urgency
   
   ## Source References

3. WHAT TO AVOID:
   - Never use: {', '.join(self.FLUFF_INDICATORS)}
   - Never use bullet points (use prose paragraphs)
   - Never make unfounded claims without evidence
   - Never provide vendor-specific recommendations

Now write the complete strategic analysis:
"""
    
    def _get_fact_extraction_prompt(self, items_context: str, title: str) -> str:
        """Pass 1: Extract key facts and synthesize themes."""
        return f"""As a Gartner analyst researching {title}, analyze the following sources and extract:

1. KEY FACTS: Specific claims, metrics, announcements, and technical details
2. STRATEGIC THEMES: What are the 3-5 major themes emerging?
3. VENDOR LANDSCAPE: Which companies are mentioned and in what context?
4. MARKET SIGNIFICANCE: Why does this matter for enterprise?

Sources:
{items_context}

Format your response as:
## Key Facts
[Specific facts with evidence]

## Strategic Themes
[3-5 themes with supporting evidence]

## Vendor Landscape
[Companies and their positioning]

## Market Significance
[Why this matters]
"""
    
    def _get_framework_prompt(
        self,
        topic: str,
        title: str,
        description: str,
        facts_and_themes: str,
        items: List[Dict],
        date: str
    ) -> str:
        """Pass 3: Apply frameworks and generate final report."""
        frameworks = self.GARTNER_FRAMEWORKS
        
        # Extract any metrics from items
        all_metrics = []
        for item in items:
            all_metrics.extend(item.get('metrics', []))
        metrics_str = ', '.join(all_metrics[:20]) if all_metrics else 'None extracted'
        
        return f"""Using your earlier analysis and the following facts, write a complete Gartner-style strategic report on {title}.

FACTS AND THEMES FROM EARLIER ANALYSIS:
{facts_and_themes}

KEY METRICS MENTIONED: {metrics_str}
Date: {date}

FRAMEWORKS TO APPLY:
- Maturity: Emerging/Trending/Mature/Declining
- Impact: Transformational/High/Moderate/Low  
- Timeline: Immediate/Near-term/Mid-term/Long-term

STRICT RULES:
1. Write in ANALYTICAL PROSE - paragraphs, not bullets
2. Apply the three frameworks above to relevant technologies
3. Include specific metrics when available
4. NO fluff words: {', '.join(self.FLUFF_INDICATORS)}
5. Be objective and evidence-based

STRUCTURE:
## Strategic Context
## Key Developments
## Technology Assessment (with maturity ratings)
## Competitive Landscape
## Risk Factors and Limitations
## Strategic Recommendations (with timeline ratings)
## Source References

Write the complete report:
"""

    # ==================== STRATEGY 3: Quality Scoring System ====================
    
    def _score_report_quality(self, report_text: str) -> float:
        """
        Score report quality 0-100 based on Gartner criteria.
        
        Criteria:
        - Prose vs bullets (Gartner style)
        - Evidence-based (specific citations, metrics)
        - Strategic recommendations
        - No fluff indicators
        """
        score = 0.0
        text_lower = report_text.lower()
        
        # 1. Prose density (25 points)
        # Count paragraph-like structures (multiple sentences)
        paragraphs = [p.strip() for p in report_text.split('\n\n') if p.strip()]
        bullet_lines = sum(1 for p in paragraphs if p.startswith('- ') or p.startswith('* '))
        if paragraphs:
            prose_ratio = 1 - (bullet_lines / len(paragraphs))
            score += 25 * min(prose_ratio * 2, 1)  # Cap at 25
        
        # 2. Evidence-based (25 points)
        evidence_indicators = [
            r'\d+%',  # Percentages
            r'\$[\d,]+',  # Dollar amounts
            r'\d+x\b',  # Ratios like 10x
            r'according to',
            r'study shows',
            r'research found',
            r'data shows',
            r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2}',
        ]
        evidence_count = sum(len(re.findall(pat, text_lower)) for pat in evidence_indicators)
        score += min(25, evidence_count * 3)  # Max 25 points
        
        # 3. Strategic recommendations (25 points)
        recommendation_indicators = ['recommend', 'should consider', 'action item', 'priority', 'strategic']
        rec_count = sum(1 for ind in recommendation_indicators if ind in text_lower)
        score += min(25, rec_count * 5)  # Max 25 points
        
        # 4. No fluff (25 points)
        fluff_count = sum(1 for word in self.FLUFF_INDICATORS if word in text_lower)
        fluff_penalty = min(25, fluff_count * 10)
        score += 25 - fluff_penalty
        
        return round(score, 1)
    
    # ==================== Original Methods (Preserved) ====================
    
    def _parse_md_items(self, md_content: str) -> List[Dict[str, Any]]:
        """Parse research items from markdown content."""
        items = []
        sections = re.split(r'^##\s+', md_content, flags=re.MULTILINE)
        
        for section in sections[1:]:
            lines = section.strip().split('\n')
            if not lines:
                continue
            
            title_match = re.match(r'^\d+\.\s+(.+)$', lines[0].strip())
            title = title_match.group(1).strip() if title_match else lines[0].strip()
            
            url = ''
            summary = ''
            source = ''
            
            for line in lines[1:]:
                url_match = re.search(r'\[Read more\]\(([^)]+)\)', line)
                if url_match:
                    url = url_match.group(1)
                
                if not line.startswith('**Source:') and not line.startswith('---'):
                    if line.strip() and not line.startswith('🔗'):
                        summary += line.strip() + ' '
            
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
    
    def _generate_rulebased_analysis(self, topic: str, items: List[Dict], date: str) -> Dict:
        """Generate analysis without LLM - rule-based synthesis."""
        topic_titles = {
            'vibe_coding': 'AI Developer Tools & Vibe Coding',
            'humanoid_robot': 'Humanoid Robotics', 
            'physical_ai': 'Physical AI & Embodied Intelligence'
        }
        
        title = topic_titles.get(topic, topic)
        themes = self._infer_themes(items)
        
        lines = [
            f"# {title}",
            f"*Gartner-Style Strategic Analysis | {date}*",
            f"*This report analyzes {len(items)} sources.*",
            "---",
            "",
            "## Strategic Context",
            f"Analysis of {len(items)} sources reveals significant developments in {topic.replace('_', ' ')}.",
            "",
        ]
        
        for theme_name, theme_items in themes.items():
            lines.extend([f"### {theme_name}", ""])
            for item in theme_items[:5]:
                lines.append(f"**{item['title']}**")
                if item.get('source'):
                    lines.append(f"*{item['source']}*")
                if item.get('summary'):
                    summary = item['summary'][:200].strip()
                    if len(item['summary']) > 200:
                        summary += "..."
                    lines.append(summary)
                if item.get('url'):
                    lines.append(f"[Source]({item['url']})")
                lines.append("")
        
        lines.extend([
            "## Risk Factors and Limitations",
            f"- {len(items)} items analyzed from multiple source types",
            f"- Themes identified: {', '.join(list(themes.keys())[:5])}",
            "",
            "## Strategic Recommendations",
            "- Monitor developments closely",
            "- Evaluate relevant use cases",
            "- Assess vendor offerings",
            "",
            "## Source References",
        ])
        
        for i, item in enumerate(items[:20], 1):
            if item.get('url'):
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
        """Infer themes from items based on keywords."""
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
        
        themes = {k: v for k, v in themes.items() if v}
        themes = dict(sorted(themes.items(), key=lambda x: len(x[1]), reverse=True))
        
        return themes
    
    def _markdown_to_html(self, md: str) -> str:
        """Convert markdown to HTML."""
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gartner-Style Strategic Analysis</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.7; color: #1a1a1a; max-width: 900px; margin: 0 auto; padding: 40px 20px; background: #f5f5f5; }
        .container { background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        h1 { font-size: 1.8em; margin-bottom: 10px; color: #1a1a1a; border-bottom: 3px solid #0066cc; padding-bottom: 15px; }
        h2 { font-size: 1.3em; margin-top: 35px; margin-bottom: 15px; color: #1a1a1a; border-bottom: 1px solid #e0e0e0; padding-bottom: 8px; }
        h3 { font-size: 1.1em; margin-top: 25px; margin-bottom: 10px; color: #333; }
        p { margin-bottom: 15px; }
        a { color: #0066cc; text-decoration: none; }
        a:hover { text-decoration: underline; }
        .meta { color: #666; font-size: 0.9em; margin-bottom: 20px; }
        ul, ol { margin-bottom: 15px; padding-left: 25px; }
        li { margin-bottom: 8px; }
        hr { border: none; border-top: 1px solid #ddd; margin: 30px 0; }
        .nav { margin-bottom: 30px; }
        .nav a { margin-right: 15px; color: #0066cc; font-weight: 500; }
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
        
        lines = md.split('\n')
        in_list = False
        
        for line in lines:
            if line.startswith('# '):
                html += f'<h1>{line[2:]}</h1>\n'
            elif line.startswith('## '):
                html += f'<h2>{line[3:]}</h2>\n'
            elif line.startswith('### '):
                html += f'<h3>{line[4:]}</h3>\n'
            elif line == '---':
                html += '<hr>\n'
            else:
                line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
                line = re.sub(r'\*(.+?)\*', r'<em>\1</em>', line)
                line = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', line)
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
        
        html += """<hr><p class="meta">Gartner-Style Strategic Analysis | AI News Aggregator</p></div></body></html>"""
        
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
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 800px; margin: 0 auto; padding: 40px 20px; background: #f5f5f5; }
        .container { background: white; padding: 40px; border-radius: 8px; }
        h1 { text-align: center; margin-bottom: 10px; color: #1a1a1a; }
        .date { text-align: center; color: #666; margin-bottom: 40px; }
        .reports { display: grid; gap: 20px; }
        .report-card { padding: 25px; border-radius: 8px; border-left: 5px solid #0066cc; background: #f8f9fa; text-decoration: none; color: inherit; transition: transform 0.2s; }
        .report-card:hover { transform: translateX(5px); }
        .report-card h2 { margin-top: 0; font-size: 1.2em; color: #0066cc; border: none; }
        .back-link { display: block; text-align: center; margin-top: 40px; color: #0066cc; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Gartner-Style Strategic Reports</h1>
        <p class="date">""" + date + """</p>
        <p style="text-align:center;margin-bottom:30px;">Analyst-level strategic analysis. Evidence-based. No fluff.</p>
        <div class="reports">
"""
        
        for topic in generated:
            title = topic_titles.get(topic, topic)
            filename = f'gartner-{topic.replace("_", "-")}.html'
            html += f'<a href="{filename}" class="report-card"><h2>{title}</h2><p>Strategic analysis →</p></a>\n'
        
        html += """</div><a href="index.html" class="back-link">← Back to Report Index</a></div></body></html>"""
        
        index_path = os.path.join(reports_dir, 'gartner-index.html')
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(html)


def generate_gartner_reports(
    web_dir: str, 
    date: str = None,
    llm_client = None,
    async_llm_client = None,
    topics: List[str] = None
) -> Dict[str, Any]:
    """Convenience function to generate Gartner-style reports."""
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
    
    generator = GartnerReportGenerator(web_dir, llm_client=llm_client, async_llm_client=async_llm_client)
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
