-- This query joins web analytics data with CRM deal data 
-- to calculate the actual Return on Investment (ROI) per source.

WITH marketing_sessions AS (
    SELECT 
        user_id,
        session_source_medium,
        landing_page,
        campaign_name,
        MIN(event_date) as first_touch_date
    FROM `your_project.ga4_data.sessions`
    GROUP BY 1, 2, 3, 4
),

crm_deals AS (
    SELECT 
        hubspot_id,
        deal_name,
        amount as deal_value,
        deal_stage,
        closed_date
    FROM `your_project.hubspot_data.deals`
    WHERE deal_stage = 'Closed Won'
)

SELECT 
    s.session_source_medium,
    COUNT(d.hubspot_id) as total_conversions,
    SUM(d.deal_value) as total_revenue,
    (SUM(d.deal_value) / COUNT(d.hubspot_id)) as average_deal_size
FROM marketing_sessions s
JOIN crm_deals d ON s.user_id = d.hubspot_id
GROUP BY 1
ORDER BY total_revenue DESC;
