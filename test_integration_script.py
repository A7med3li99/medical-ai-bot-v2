
import requests

# Test: Predict disease based on symptoms
def test_predict_disease():
    url = 'http://127.0.0.1:5000/predict_disease'
    symptoms = [1, 0, 1]
    response = requests.post(url, json={'symptoms': symptoms})
    if response.status_code == 200:
        print('Disease Prediction Test Passed:', response.json())
    else:
        print('Disease Prediction Test Failed:', response.status_code, response.text)

# Test: Extended diagnose with treatment and drug interactions
def test_extended_diagnose():
    url = 'http://127.0.0.1:7000/bot/extended_diagnose'
    data = {
        'symptoms': [1, 0, 1],
        'drugs': ['Drug_A', 'Drug_B']
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print('Extended Diagnose Test Passed:', response.json())
    else:
        print('Extended Diagnose Test Failed:', response.status_code, response.text)

# Run all tests
if __name__ == '__main__':
    print('Running tests...')
    test_predict_disease()
    test_extended_diagnose()
