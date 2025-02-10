import requests
import json
def hindi2english(hindi_text, model='llama3:8b'):
    if len(hindi_text) == 0: return hindi_text
    headers = {"Content-Type": "application/json"}
    params = {"model": model, "prompt": 'Translate the text from hindi to English and only return the content translated. There should be no explanation. Output should be inproper json format.Example: {"translated":"aa"}.'+hindi_text, "stream": False,
              }
    resp = requests.post('http://localhost:11434/api/generate', headers=headers, data=json.dumps(params))
    if resp.status_code == 200:
        resp = resp.json()
        try:
           resp = json.loads(resp['response'])
           return resp['translated']
        except:
            return resp['response']


    return hindi_text

#print(hindi2english("उत्तर प्रदेश संस्कृति, समृद्धि और संभावनाओं की धरती, जहाँ इतिहास के स्वर्णिम पृष्ठों से भविष्य के उज्ज्वल सपने लिखे जाते है, आज एक नई आर्थिक दृष्टि और ऊर्जा के साथ अपने लक्ष्यों की ओर अग्रसर है। प्रदेश की अर्थव्यवस्था 24 करोड़ से अधिक लोगों की आकांक्षाओं का प्रतिबिंब है, जो इसे कृषि संपन्नता, औद्योगिक प्रगति और तकनीकी नवाचार का केंद्र बना रही है। उर्वर गंगा-यमुना के मैदानों में फैला उत्तर प्रदेश, खाद्यान्न, गन्ना, आम, दुग्ध, तिलहन एवं आलू के उत्पादन में अग्रणी भूमिका के साथ भारत का अन्न भंडार कहलाता है। हरे-भरे खेत और मेहनतकश किसान उत्तर प्रदेश को न केवल आत्मनिर्भर बनाते हैं बल्कि भारत की खाद्य सुरक्षा में भी महत्वपूर्ण भूमिका निभाते हैं। यहाँ की गन्ना आधारित चीनी उद्योग ने वैश्विक स्तर पर प्रदेश को एक प्रमुख केंद्र बना दिया है।"))