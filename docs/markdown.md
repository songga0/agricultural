# My API Documentation

## /predict
- **Method:** POST
- **Description:** Endpoint for predicting the grade of agricultural products.

### Request
- **URL:** `/predict`
- **Parameters:**
  - `file` (multipart/form-data): Image file for prediction.

#### Request Example (cURL):
```bash
curl -X POST -F "file=@/path/to/your/image.png" http://your-api-url/predict

### Response
- **Status Code:** 200 OK
- **Body:** JSON object with predicted label.

## /protected
...
