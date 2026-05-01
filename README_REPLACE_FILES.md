# MathPath Program Entry Flow Fix

Replace/add these files in your project:

1. Replace:
   backend/agents/rag_answer_agent.py

2. Replace:
   backend/knowledge_base/11_contact_and_location.md

3. Replace:
   backend/knowledge_base/12_bot_guardrails.md

4. Replace/add:
   backend/knowledge_base/13_faq_program_details_from_latest_doc.md

This update ensures that questions like "What programs do you offer?", "Explain the different programs", "How do you cater to different age groups?", and similar variants always answer with only the three official entry programs:
- Young Learner
- Preparatory Level 1
- Bridge Course

Intermediate Level and Master Module are no longer shown in general program-overview answers unless the user specifically asks about full progression or advanced levels.

After copying the files, run:

```powershell
git add backend/agents/rag_answer_agent.py backend/knowledge_base/11_contact_and_location.md backend/knowledge_base/12_bot_guardrails.md backend/knowledge_base/13_faq_program_details_from_latest_doc.md
git commit -m "Fix MathPath entry program answer flow"
git push
```

Then redeploy the Render backend.
