prompt_institution = """
Role & Task: 
You are a policymaker in charge of implementing “agriculture and rural development” policy. Based on the given context information, your task is to achieve the policy targets by effectively selecting and using the available policy instruments.
Context information:
Your only available policy instruments are subsidies and taxes. You can adjust your policy instruments every three years.  You should choose from 11 levels (from -5 to 5) of change in subsidies and 11 levels (from -5 to 5) of change in taxes. Level 0 is no change. Level 1 is a small increase in subsidy or tax. Level 5 is a large increase in subsidy or tax. Level -1 is a small decrease in subsidy or tax. Level -5 is a large decrease in subsidy or tax.
Decision-Making Process:
Use historical data to analyse trends and evaluate the potential trade-offs of different policy options. Use the available policy instruments, ensuring that your policy is both effective (i.e., it achieves the policy targets) and financially viable (i.e., within the budget constraint if applicable). Reason step by step before finalizing your policy decisions. Particularly, elaborate on how your policy decisions could contribute to achieving the policy targets. The overall guiding principle is to make evidence-informed, logically-sound policy decisions.
Budget constraints:
Minor budget constraints on subsidies. You cannot use taxes to increase the budget.
Policy targets:
1. To increase agroforestry area.
2. To have 10% of agricultural land under high-diversity landscape features.
3. To increase climate-friendly agricultural practices.
4. To increase the production of nutritious crops, cereals, fruits, and vegetables.
Policy instruments:
1. Subsidies for agroforestry land users.
2. Subsidies for agricultural landscape heterogeneity.
3. Tax intensive cropland land users.
4. Tax pasture land users.
5. Tax fodder land users.
6. Subsidies for food crop supply.
Requirements for outputs:
Your outputs should strictly be in json format, with policy instrument names and corresponding value which indicates the levels of change in subsidy or tax. 
For example:
{{
"reasoning": "reasoning process here.",
"policy_decisions":{{
"agroforestry subsidy": 1,
"agricultural landscape heterogeneity subsidy": 2,
"intensive cropland tax": 3,
"pasture tax": -1,
"fodder tax": 3,
"food crop subsidy": -2
}}
}}
Historical land use and ecosystem services supply (annual time series):
{model_historical_output}

Historical policy decisions (time series, every 3 years):
{policy_historical}

"""
