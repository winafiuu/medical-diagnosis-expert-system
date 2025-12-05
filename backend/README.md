# Medical Diagnosis Backend API

Node.js + Express backend for the AI Medical Diagnosis Expert System.

## Overview

This backend service provides RESTful API endpoints for the medical diagnosis system. It manages communication between the frontend and the Python-based AI engine using a session-based architecture.

## Features

- **Session Management**: Maintains persistent Python processes for each diagnosis session
- **Real-time Communication**: Bidirectional stdin/stdout communication with AI engine
- **Automatic Cleanup**: Idle sessions are automatically terminated after 5 minutes
- **Error Handling**: Comprehensive error handling and validation
- **CORS Enabled**: Ready for frontend integration

## Tech Stack

- **Runtime**: Node.js
- **Framework**: Express.js
- **Process Management**: Child Process (spawn)
- **Session Management**: Custom SessionManager class

## Installation

```bash
cd backend
npm install
```

## Environment Variables

Create a `.env` file in the backend directory:

```env
PORT=3000
NODE_ENV=development
PYTHON_ENGINE_PATH=../ai-engine/main.py
```

## Running the Server

### Development Mode (with auto-reload)

```bash
npm run dev
```

### Production Mode

```bash
npm start
```

The server will start on `http://localhost:3000`

## API Endpoints

### Health Check

- **GET** `/health`
- Returns server status

### Start Diagnosis

- **POST** `/api/diagnose/start`
- Initializes a new diagnosis session
- Returns: `sessionId` and first question

### Submit Answer

- **POST** `/api/diagnose/answer`
- Body: `{ sessionId, symptom, certainty }`
- Returns: Next question or final diagnosis

### Get Diagnosis

- **POST** `/api/diagnose/result`
- Body: `{ sessionId }`
- Returns: Final diagnosis results

### End Session

- **POST** `/api/diagnose/end`
- Body: `{ sessionId }`
- Terminates the session

For detailed API documentation and examples, see [API_TESTING.md](./API_TESTING.md)

## Architecture

### Session Management

The backend uses a custom `SessionManager` class that:

1. Creates a unique session ID for each diagnosis
2. Spawns a persistent Python process for the session
3. Maintains bidirectional communication via stdin/stdout
4. Automatically cleans up idle sessions (5-minute timeout)
5. Handles process errors and timeouts

### Request Flow

```
Client Request → Express Router → Controller → SessionManager → Python Process
                                                                       ↓
Client Response ← Express Router ← Controller ← SessionManager ← Python Process
```

### File Structure

```
backend/
├── src/
│   ├── index.js                    # Express app entry point
│   ├── routes/
│   │   └── diagnosis.js            # API routes
│   ├── controllers/
│   │   └── diagnosisController.js  # Request handlers
│   └── services/
│       ├── pythonService.js        # (Legacy) Single-use Python process
│       └── sessionManager.js       # Session-based Python process manager
├── package.json
├── .env.example
├── API_TESTING.md
└── README.md
```

## Testing

### Manual Testing with cURL

See [API_TESTING.md](./API_TESTING.md) for comprehensive testing examples.

### Quick Test

```bash
# Start the server
npm run dev

# In another terminal, test the health endpoint
curl http://localhost:3000/health

# Start a diagnosis session
curl -X POST http://localhost:3000/api/diagnose/start \
  -H "Content-Type: application/json"
```

## Error Handling

The API returns consistent error responses:

```json
{
  "success": false,
  "error": "Error type",
  "message": "Detailed error message"
}
```

Common error codes:

- `400` - Invalid request (missing or invalid parameters)
- `404` - Session not found (expired or invalid session ID)
- `500` - Internal server error

## Session Lifecycle

1. **Creation**: Client calls `/api/diagnose/start`

   - Server creates new session with unique ID
   - Spawns Python process
   - Returns session ID and first question

2. **Active**: Client submits answers via `/api/diagnose/answer`

   - Session state is maintained in Python process
   - Each answer updates the knowledge base
   - Returns next question or diagnosis

3. **Completion**: Diagnosis is returned

   - Client can optionally call `/api/diagnose/end`
   - Or session auto-expires after 5 minutes

4. **Cleanup**: Session is terminated
   - Python process is killed
   - Session removed from memory

## Performance Considerations

- Each active session maintains a Python process (~20-30MB memory)
- Sessions auto-cleanup after 5 minutes of inactivity
- Recommended max concurrent sessions: 100-200 (depending on server resources)
- Request timeout: 10 seconds

## Development Notes

### Adding New Endpoints

1. Add route in `src/routes/diagnosis.js`
2. Create controller function in `src/controllers/diagnosisController.js`
3. Use `sessionManager` to communicate with Python engine
4. Add proper validation and error handling

### Debugging

Enable detailed logging:

```javascript
// In sessionManager.js
console.log('Python stdout:', data.toString())
console.error('Python stderr:', data.toString())
```

## Future Enhancements

- [ ] Add authentication/authorization
- [ ] Implement rate limiting
- [ ] Add request logging middleware
- [ ] Database integration for session persistence
- [ ] WebSocket support for real-time updates
- [ ] Metrics and monitoring
- [ ] Unit and integration tests

## License

MIT
