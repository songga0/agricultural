# My API Documentation

## Image Requirements:
- **Image Size:** 64x64 pixels
- **Color Channels:** RGB format

## /predict
- **Method:** POST
- **Description:** Endpoint for predicting the grade of agricultural products.

### Request
- **URL:** `/predict`
- **Parameters:**
  - `file` (multipart/form-data): Image file for prediction.
  - `threshold` (float, optional): Confidence threshold for predictions. Default is 0.5.
- **Authentication:** API Key

#### Request Example (cURL):
```bash
curl -X POST -F "file=@/path/to/your/image.png" -F "threshold=0.7" -H "Authorization: your_api_key" http://your-api-url/predict

### Response
- **Status Code:** 200 OK
- **Body:** JSON object with predicted label.

### Response Example
```json
{
  "predicted_label": "Grade A"
}

## /protected
- **Method:** GET
- **Description:** Protected endpoint requiring admin privileges.
- **Authentication:** Bearer Token

#### Request Example (cURL):
```bash
curl -X GET -H "Authorization: Bearer your_access_token" http://your-api-url/protected

### Response
- **Status Code:** 200 OK
- **Body:**JSON object with protected resource message.

### Error Responses
- **Status Code:** 400 Bad Request
  - **Body:** `{"error": "Invalid file or file size exceeded"}`
  - **Description:** The uploaded file is invalid or exceeds the allowed size.

- **Status Code:** 401 Unauthorized
  - **Body:** `{"error": "Invalid API key"}`
  - **Description:** The provided API key is invalid.

- **Status Code:** 500 Internal Server Error
  - **Body:** `{"error": "Internal Server Error"}`
  - **Description:** An unexpected error occurred on the server.
