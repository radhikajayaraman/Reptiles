import requests

re=requests.get('http://stagingapi.amagimix.com:2770/compute-media-package?regions=Uttar Pradesh, Gujarat, Orissa, North East, Mumbai, Pun/Har/Cha/HP/J%26K, Madhya Pradesh, Delhi NCR, Rajasthan, West Bengal, TN/Pondicherry, Maharashtra/Goa, Chhattisgarh, Bangalore, Kerala&date=21-10-16&gender=Male, Female&sub_category=Banking/Finance/Investment&profile=College Adults&duration=8&spot_duration=10&budgets=85473&user_id=radhika@amagi.com')
print re.text
