import json
import random
from xml.etree import ElementTree as ET


def generate_weather_data(cities):
    """
    Generates random weather data for given cities
    Returns: Dictionary {city: {temperature, humidity, condition}}
    """
    weather_data = {}
    conditions = ['sunny', 'cloudy', 'rainy', 'snowy', 'foggy', 'stormy']
    
    for city in cities:
        weather_data[city] = {
            'temperature': round(random.uniform(-10, 35)),  
            'humidity': random.randint(30, 100),           
            'condition': random.choice(conditions)
        }
    return weather_data


def format_json(weather_data):
    """Converts weather data to JSON format"""
    return json.dumps(weather_data, indent=2)


def format_xml(weather_data):
    """Converts weather data to XML format"""
    root = ET.Element('WeatherData')
    
    for city, data in weather_data.items():
        city_elem = ET.SubElement(root, 'City', name=city)
        
        ET.SubElement(city_elem, 'Temperature').text = str(data['temperature'])
        ET.SubElement(city_elem, 'Humidity').text = str(data['humidity'])
        ET.SubElement(city_elem, 'Condition').text = data['condition']
    
    
    ET.indent(root, space="\t", level=0)
    return ET.tostring(root, encoding='unicode', xml_declaration=True)


XML_SCHEMA = """<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="WeatherData">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="City" maxOccurs="unbounded" minOccurs="1">
          <xs:complexType>
            <xs:sequence>
              <xs:element name="Temperature" type="xs:decimal"/>
              <xs:element name="Humidity" type="xs:integer"/>
              <xs:element name="Condition" type="xs:string"/>
            </xs:sequence>
            <xs:attribute name="name" type="xs:string" use="required"/>
          </xs:complexType>
        </xs:element>
      </xs:sequence>
    </xs:complexType>
  </xs:element>
</xs:schema>"""

if __name__ == "__main__":
  
    cities = ["Nairobi", "Cape town", "Cairo", "Lusaka", "Accra", "Lagos"]
    
    
    weather_data = generate_weather_data(cities)
    
    
    json_output = format_json(weather_data)
    print("="*50)
    print("JSON Weather Data:")
    print("="*50)
    print(json_output)
    
    
    xml_output = format_xml(weather_data)
    print("\n" + "="*50)
    print("XML Weather Data:")
    print("="*50)
    print(xml_output)
    
  
    print("\n" + "="*50)
    print("XML Schema Definition:")
    print("="*50)
    print(XML_SCHEMA)