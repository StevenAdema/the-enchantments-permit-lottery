# 🏕️Enchantments Permit Lottery

Wilderness permits for the rugged and beautiful Enchantment Permit Area can be extremely difficult to obtain. On the most popular days, only <b>1 in 400</b> applications was awarded a permit!

Each permit entry costs $6 USD and is limited to one per person. I've collected information from the lottery statistics data published byt te USDA Forest Service to help you make the best selection possible. 

I'm making my code and .csv files available which are much more useful than the 520 page PDF file provided by USDA Forest Service. 

### ⛰️Enchantments Overview
Permits are required to for overnight camping in the Enchantment Permit Area between May 15 and Oct 31. Due to the extremely high demand permits are awarded via a lottery that opperates from Feb 15 - 29, 2024.

For more information about the permits, permit zones and how the lottery operates see https://www.recreation.gov/permits/233273.

### 🎟️Quick Lottery Stats (2023)
- <b>6.8%</b> of all applications were awarded (2,558 out of 37,474).
- Sunday permits are <b>4X</b> more likely to be awarded than Friday permits.
- July, Aug, and Sep permits are <b>more than twice</b> as hard to obtain compared to Jun or Oct.
- The lowest success rate is from the <b>Core Enchantment Zone</b> (1%). Highest is <b>Eightmile/Caroline Zone</b> (12%)

### 🍀Lottery Selection Tool: Heatmap
View the probabilty of a permit date and zone being awarded a permit as a heatmap. 

E.g. I am booking a trip during the final week of July. I am available to hike on any of July-22 through July-28. My preference is Core Zone, but I am ok with Stuart zone if the probability of a successfully awarded ticket is 9% compared to just 2% in core for the same date (07-23, Sun).
<img src='/img/heatmap-4.png' width=100%>

### 🍀Lottery Selection Tool: Probability Distribution
Simulate the permit lottery to view the frequency of at least one permit being awarded. This is very useful if you have made many or varied entries.

E.g. I, along with two friends, made 3 permit applications with 3 choices each (9 total). Our choices are entered in the var <b>lottery_dic</b> on line 27 of main.py. The plot_distribution() function will run the lottery simulation *n* times and plot the frequency of permit awarding.
```
lottery_dic = [
    {'date': '2023-06-20', 'zone':'Snow Zone', 'n': 3},
    {'date': '2023-06-21', 'zone':'Snow Zone', 'n': 3},
    {'date': '2023-06-22', 'zone':'Stuart Zone', 'n': 2},
    {'date': '2023-06-20', 'zone':'Core Zone', 'n': 1}
]
```
In 755 of 1000 simulations we are awarded at least *one* of our choices.
<img src='/img/distribution.png' width=100%>
<br>
<br>
##📅Full Heatmap Calendar
See below for the rates of successful permit applications by date and zone for permits in 2023.
<img src='/img/heatmap-3.png' width=100%>

lottery_dic = [
        {'date': '2023-06-20', 'zone':'Snow Zone', 'n': 3},
        {'date': '2023-06-21', 'zone':'Snow Zone', 'n': 3},
        {'date': '2023-06-22', 'zone':'Stuart Zone', 'n': 2},
        {'date': '2023-06-20', 'zone':'Core Zone', 'n': 1}
    ]
'''
In 755 of 1000 simulations we are awarded at least *one* of our choices.
<img src='/img/distribution.png' width=100%>
<br>
<br>
##📅Full Heatmap Calendar
See below for the rates of successful permit applications by date and zone for permits in 2023.
<img src='/img/heatmap-3.png' width=100%>
