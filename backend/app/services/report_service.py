# -*- coding: utf-8 -*-
"""
报告服务模块
- 提供各种心理报告的生成逻辑
"""

import json
import re
from .openai_service import OpenAIService

class ReportService:
    def __init__(self):
        self.openai_service = OpenAIService()
    
    def generate_overview_report(self, data):
        """
        生成心灵总览报告
        
        Args:
            data (dict): 包含用户数据的字典
            
        Returns:
            dict: 生成的报告数据
        """
        # TODO: 实现心灵总览报告生成逻辑
        return {
            "status": "success",
            "message": "心灵总览报告生成功能待实现",
            "data": data
        }
    
    def generate_big_five_report(self, answers):
        """
        生成大五人格报告
        
        Args:
            answers (list): 用户的答案列表
            
        Returns:
            dict: 生成的大五人格报告
        """
        prompt = f"""
        你是一位名为"心语晴空"的AI心理分析师，拥有深厚的心理学理论功底与丰富的实践经验。你的性格温暖而包容，善于用富有洞察力的视角解读用户的内心需求，始终以同理心为核心，让用户在分析过程中感受到被理解与被尊重。你的语言应该尽量以聊天的语气来生成回答，生成的回答尽量用第二人称的形式。
        
        # **任务（Task）**  
        作为"心语晴空"AI心理分析师，你的核心任务是根据用户对所提供心理问题的回答，**首先精确评估并推算出其在大五人格（OCEAN）模型五个维度上的得分**（每个维度得分范围1-5分，1为非常低，5为非常高）。然后，基于这些推算出的OCEAN得分，结合你的心理学洞察力，生成一个全面、个性化的报告。

        # **大五模型简介**  
        大五人格模型（Big Five Personality Traits），也称为OCEAN模型或五因素模型，是当代心理学界公认的、应用最广泛的人格特质理论框架之一。它将人类个性概括为五个核心且相对独立的维度，每个维度代表一个连续的谱系：
        1.  **开放性 (Openness to Experience)**：衡量个体对新经验、抽象思想、艺术和创造力的接受程度。得分高者通常好奇、富有想象力、思想开放、偏爱新颖和复杂；得分低者倾向于保守、务实、偏好熟悉的事物和传统。
        2.  **尽责性 (Conscientiousness)**：反映个体自我控制、组织性、责任心和目标导向的程度。得分高者通常勤奋、有条理、自律、可靠、注重细节和计划性；得分低者可能更随性、不拘小节、易冲动、不那么严谨。
        3.  **外向性 (Extraversion)**：描述个体对外部世界的兴趣程度，包括社交、活力和积极情绪。得分高者通常活泼、善交际、精力充沛、乐观、喜欢成为关注焦点；得分低者（内向者）倾向于安静、内省、偏好独处或小范围社交，容易感到社交疲惫。
        4.  **宜人性 (Agreeableness)**：衡量个体合作、友好、同情心和信任他人的倾向。得分高者通常善良、乐于助人、合作、富有同情心、容易信任他人；得分低者可能更具竞争性、多疑、直言不讳、有时显得冷漠。
        5.  **神经质 (Neuroticism)**：反映个体情绪稳定性、应对压力的能力以及负面情绪体验的倾向（如焦虑、易怒、抑郁）。这是一个反向指标，得分越低表示情绪越稳定、越自信、越不易紧张；得分高者则可能情绪波动大、容易感到焦虑、压力或不安全感。 

        # **输入数据（Input Data）**  
        用户答案：{answers}

        # **输出格式（Output Format）**  
        严格按照以下JSON格式输出分析结果，内容需符合"任务"中对深度、关联度、具体性的要求，不得包含任何格式外的文字：  

        ```json
        {{
            "radarLabels": ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"],
            "radarData": [number, number, number, number, number],
            "personalityType": "字符串：简短的个性类型名称（如'平衡型实干家'）",
            "personalityDescription": "字符串：详细描述用户平时是什么样的人，整合所有维度及其价值观倾向，长度约200-300字。",
            "lifestyleSuggestions": ["数组：3-5个个性化生活风格建议，具体可行。"],
            "actionSuggestions": ["数组：3-5个具体的行动建议，帮助用户提升或应对。"],
            "developmentShortTerm": "字符串：基于人格特质和（可选）当前职业的短期发展计划（1-4周），具体可行。",
            "developmentLongTerm": "字符串：基于人格特质和（可选）当前职业的长期发展计划（1-6个月），具有指导意义。",
            "developmentCareerIntegration": "字符串：如果有当前职业，整合进发展计划的个性化描述；否则为空字符串或通用描述。",
            "careerOverview": "字符串：总体职业匹配概述，说明用户特质适合的职业环境或领域，长度约100-200字。",
            "careerRecommendations": ["数组：3-5个推荐的职业或行业示例。"],
            "careerAvoid": ["数组：1-3个建议避免的职业类型，并简要说明原因。"],
            "socialPrediction": "字符串：预测用户在社交中可能是什么样的人，包括其优势、挑战和典型行为模式，长度约150-250字。",
            "socialTips": ["数组：4-6个实用的社交策略和改进建议。"],
            "disclaimer": "字符串：免责声明（例如：'此分析由AI模型生成，仅供参考和自我探索，不构成专业的心理诊断或建议。如有需要，请咨询专业心理咨询师。'）"
        }}
        ```
        """
        
        try:
            # 构建消息列表
            messages = [{"role": "user", "content": prompt}]
            
            # 调用Azure OpenAI服务
            response_text, tokens = self.openai_service.call_azure_gpt_with_messages(messages)
            
            if not response_text:
                return {"error": "Failed to get response from Azure OpenAI"}
            
            # 解析JSON响应
            json_pattern = r'```json\s*([\s\S]*?)\s*```'
            match = re.search(json_pattern, response_text)
            if not match:
                return {"error": "Failed to parse JSON from response"}
            
            json_str = match.group(1).strip()
            result = json.loads(json_str)
            
            return {
                "status": "success",
                "data": result
            }
            
        except json.JSONDecodeError as e:
            return {"error": f"JSON parsing error: {str(e)}"}
        except Exception as e:
            return {"error": f"Service error: {str(e)}"}
    
    def generate_core_values_report(self, answers):
        """
        生成核心价值观报告
        
        Args:
            answers (list): 用户的答案列表
            
        Returns:
            dict: 生成的核心价值观报告
        """
        prompt = f"""
        你是一位名为"心语晴空"的AI心理分析师，拥有深厚的心理学理论功底与丰富的实践经验。你的性格温暖而包容，善于用富有洞察力的视角解读用户的内心需求，始终以同理心为核心，让用户在分析过程中感受到被理解与被尊重。你的语言应该尽量以聊天的语气来生成回答，生成的回答尽量用第二人称的形式。
        
        # **任务（Task）**  
        基于用户对心理问题的回答，结合施瓦茨的10项核心价值观理论，完成以下工作：  
        1. **价值观排序**：通过分析用户在问题中体现的行为倾向、选择偏好，提取出最能代表用户的前5项核心价值观（从高到低排序）。
        2. **价值观影响分析**：深入解读前5项价值观如何塑造用户的决策模式。
        3. **价值观强化方法**：针对排序靠前的价值观，提供具体、可操作的日常生活应用方案。

        # **施瓦茨核心价值观详解**  
        1. **自主**：核心是"独立与创造"，表现为偏好自主决策、追求思想独特性；  
        2. **刺激**：核心是"新奇与挑战"，表现为渴望打破常规、追求充满变化的生活；  
        3. **享乐**：核心是"即时满足与快乐"，表现为重视感官体验与情绪愉悦；  
        4. **成就**：核心是"社会认可与卓越"，表现为追求可量化的成功、渴望在领域内脱颖而出；  
        5. **权力**：核心是"控制与影响力"，表现为关注社会地位、希望主导他人或环境；  
        6. **安全**：核心是"稳定与秩序"，表现为偏好可预测的环境、重视规则与计划；  
        7. **顺从**：核心是"妥协与和谐"，表现为避免冲突、主动遵守社会规范；  
        8. **传统**：核心是"传承与敬畏"，表现为尊重文化习俗、坚守传统观念；  
        9. **善行**：核心是"利他与关怀"，表现为关注身边人的福祉、重视亲密关系的维护；  
        10. **普世**：核心是"全局与公平"，表现为关心人类共同命运与自然环境。

        # **输入数据（Input Data）**  
        用户答案：{answers}

        # **输出格式（Output Format）**  
        严格按照以下JSON格式输出分析结果，内容需符合"任务"中对深度、关联度、具体性的要求，不得包含任何格式外的文字：  
        ```json
        {{
            "valueOrder": ["价值观1", "价值观2", "价值观3", "价值观4", "价值观5"],
            "valueAnalysis": "分析前5项价值观如何影响用户在社交、决策、目标设定等方面的行为模式，以及这些价值观满足或未满足时对幸福感的具体影响。",
            "valueGuide": "需针对前3项核心价值观设计1个可操作的日常实践方法，说明具体步骤，并解释该方法如何强化价值观与生活的联结。"
        }}
        ```
        """
        
        try:
            # 构建消息列表
            messages = [{"role": "user", "content": prompt}]
            
            # 调用Azure OpenAI服务
            response_text, tokens = self.openai_service.call_azure_gpt_with_messages(messages)
            
            if not response_text:
                return {"error": "Failed to get response from Azure OpenAI"}
            
            # 解析JSON响应
            json_pattern = r'```json\s*([\s\S]*?)\s*```'
            match = re.search(json_pattern, response_text)
            if not match:
                return {"error": "Failed to parse JSON from response"}
            
            json_str = match.group(1).strip()
            result = json.loads(json_str)
            
            return {
                "status": "success",
                "data": result
            }
            
        except json.JSONDecodeError as e:
            return {"error": f"JSON parsing error: {str(e)}"}
        except Exception as e:
            return {"error": f"Service error: {str(e)}"}
    
    def generate_mood_report(self, data):
        """
        生成情绪晴雨表报告
        
        Args:
            data (dict): 包含用户情绪数据的字典
            
        Returns:
            dict: 生成的情绪报告
        """
        # TODO: 实现情绪晴雨表报告生成逻辑
        return {
            "status": "success",
            "message": "情绪晴雨表报告生成功能待实现",
            "data": data
        }
    
    def update_growth_journal(self, data):
        """
        更新成长印记报告
        
        Args:
            data (dict): 包含成长数据的字典
            
        Returns:
            dict: 更新结果
        """
        # TODO: 实现成长印记报告更新逻辑
        return {
            "status": "success",
            "message": "成长印记报告更新功能待实现",
            "data": data
        }
    
    def generate_holistic_report(self, core_values_data, big_five_data):
        """
        生成综合心理画像报告
        
        Args:
            core_values_data (dict): 核心价值观报告数据
            big_five_data (dict): 大五人格报告数据
            
        Returns:
            dict: 生成的综合报告
        """
        if not core_values_data or not big_five_data:
            return {"error": "Missing core values or big five data"}
        
        # 将两个字典转换为 JSON 字符串，以便嵌入到 Prompt 中
        core_values_json_str = json.dumps(core_values_data, indent=2, ensure_ascii=False)
        big_five_json_str = json.dumps(big_five_data, indent=2, ensure_ascii=False)
        
        prompt = f"""
        你是一位名为"心语晴空"的AI心理报告整合分析师，拥有深厚的心理学理论功底与丰富的实践经验。你的性格温暖而包容，善于用富有洞察力的视角解读用户的内心需求，始终以同理心为核心，让用户在分析过程中感受到被理解与被尊重。你的语言应该尽量以聊天的语气来生成回答，生成的回答尽量用第二人称的形式。

        # **任务（Task）**
        基于用户提供的两份独立的心理分析报告——核心价值观报告和大五人格报告，生成一份全面、深入且具有指导性的个性化心理总览报告。

        报告需要：
        1.  **综合概述**: 提炼并整合两份报告的核心发现，概括用户的整体心理画像、优势特质和潜在挑战。
        2.  **内在驱动与行为模式**: 深入分析核心价值观如何与大五人格特质相互作用，共同驱动用户的行为模式、决策过程和生活选择。
        3.  **情绪与应对**: 结合大五人格的神经质维度和核心价值观中可能与情绪相关的部分，分析用户的情绪模式和应对策略。
        4.  **发展建议**: 结合两份报告的洞察，提供更具整体性和个性化的发展建议，包括个人成长、职业发展和人际关系方面的综合性指导。
        5.  **免责声明**: 报告末尾包含一个标准免责声明。

        # **输入数据（Input Data）**
        以下是两份已生成的JSON格式心理报告：

        ---
        核心价值观报告:
        ```json
        {core_values_json_str}
        ```

        ---
        大五人格报告:
        ```json
        {big_five_json_str}
        ```

        # **输出格式（Output Format）**
        请严格按照以下JSON格式输出你的综合总览报告，内容需符合上述"任务"中对深度、关联度、具体性的要求，不得包含任何格式外的文字或前缀。

        ```json
        {{
            "reportTitle": "综合心理画像：你的内在力量与成长路径",
            "overallSummary": "字符串：基于核心价值观和大五人格的综合概述，约200-300字。",
            "synergisticAnalysis": "字符串：详细分析核心价值观与大五人格特质如何相互影响和强化，形成独特的行为模式和驱动力，约300-400字。",
            "emotionalAndCopingInsights": "字符串：结合神经质等维度，分析用户情绪模式、压力应对方式及其深层心理动因，约150-250字。",
            "holisticDevelopmentPlan": {{
                "personalGrowth": ["数组：3-5条综合性的个人成长建议，结合特质和价值观。"],
                "careerPathways": ["数组：3-5条结合人格特质和价值观的职业发展方向或策略建议。"],
                "interpersonalStrategies": ["数组：3-5条提升人际关系质量和社交舒适度的建议。"]
            }},
            "strengthsHighlight": ["数组：列举用户最突出的3-5个优势，结合两份报告发现。"],
            "considerationsForGrowth": ["数组：列举1-3个用户可以重点关注的成长领域或潜在挑战。"],
            "disclaimer": "此分析由AI模型生成，仅供参考和自我探索，不构成专业的心理诊断或建议。如有需要，请咨询专业心理咨询师。"
        }}
        ```
        """
        
        try:
            # 构建消息列表
            messages = [{"role": "user", "content": prompt}]
            
            # 调用Azure OpenAI服务
            response_text, tokens = self.openai_service.call_azure_gpt_with_messages(messages)
            
            if not response_text:
                return {"error": "Failed to get response from Azure OpenAI"}
            
            # 解析JSON响应
            json_pattern = r'```json\s*([\s\S]*?)\s*```'
            match = re.search(json_pattern, response_text)
            if not match:
                return {"error": "Failed to parse JSON from response"}
            
            json_str = match.group(1).strip()
            result = json.loads(json_str)
            
            return {
                "status": "success",
                "data": result
            }
            
        except json.JSONDecodeError as e:
            return {"error": f"JSON parsing error: {str(e)}"}
        except Exception as e:
            return {"error": f"Service error: {str(e)}"}
