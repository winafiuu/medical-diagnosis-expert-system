/**
 * Session Manager for maintaining diagnosis sessions
 * Each session maintains a persistent Python process
 */

import { spawn } from 'child_process'
import path from 'path'
import { fileURLToPath } from 'url'
import { randomUUID } from 'crypto'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

class DiagnosisSession {
  constructor(sessionId) {
    this.sessionId = sessionId
    this.pythonProcess = null
    this.isActive = false
    this.pendingRequests = []
    this.lastActivity = Date.now()
  }

  /**
   * Start the Python process for this session
   */
  start() {
    return new Promise((resolve, reject) => {
      const scriptPath =
        process.env.PYTHON_ENGINE_PATH ||
        path.join(__dirname, '../../../ai-engine/main.py')

      const pythonExecutable = process.env.PYTHON_EXECUTABLE || 'python'

      this.pythonProcess = spawn(pythonExecutable, [scriptPath])
      this.isActive = true

      let startupComplete = false

      // Handle stdout data
      this.pythonProcess.stdout.on('data', (data) => {
        const lines = data
          .toString()
          .split('\n')
          .filter((line) => line.trim())

        lines.forEach((line) => {
          if (this.pendingRequests.length > 0) {
            const { resolve: pendingResolve } = this.pendingRequests.shift()
            try {
              const result = JSON.parse(line)
              pendingResolve(result)
            } catch (error) {
              pendingResolve({
                status: 'error',
                message: `Failed to parse response: ${error.message}`,
              })
            }
          }
        })
      })

      // Handle stderr
      this.pythonProcess.stderr.on('data', (data) => {
        console.error(`Python stderr [${this.sessionId}]:`, data.toString())
      })

      // Handle process exit
      this.pythonProcess.on('close', (code) => {
        this.isActive = false
        console.log(
          `Python process [${this.sessionId}] exited with code ${code}`
        )

        // Reject all pending requests
        this.pendingRequests.forEach(({ reject }) => {
          reject(new Error('Python process terminated'))
        })
        this.pendingRequests = []
      })

      // Handle process errors
      this.pythonProcess.on('error', (error) => {
        this.isActive = false
        if (!startupComplete) {
          reject(new Error(`Failed to start Python process: ${error.message}`))
        }
      })

      // Initialize the session
      this.sendCommand({ action: 'start' })
        .then((result) => {
          startupComplete = true
          resolve(result)
        })
        .catch((error) => {
          startupComplete = true
          reject(error)
        })
    })
  }

  /**
   * Send a command to the Python process
   */
  sendCommand(command) {
    return new Promise((resolve, reject) => {
      if (!this.isActive || !this.pythonProcess) {
        reject(new Error('Session is not active'))
        return
      }

      this.lastActivity = Date.now()

      // Add to pending requests queue
      this.pendingRequests.push({ resolve, reject })

      // Set timeout for this request
      const timeout = setTimeout(() => {
        const index = this.pendingRequests.findIndex(
          (r) => r.resolve === resolve
        )
        if (index !== -1) {
          this.pendingRequests.splice(index, 1)
          reject(new Error('Request timeout'))
        }
      }, 10000)

      // Clear timeout when resolved
      const originalResolve = resolve
      const wrappedResolve = (result) => {
        clearTimeout(timeout)
        originalResolve(result)
      }
      this.pendingRequests[this.pendingRequests.length - 1].resolve =
        wrappedResolve

      // Send command
      try {
        this.pythonProcess.stdin.write(JSON.stringify(command) + '\n')
      } catch (error) {
        clearTimeout(timeout)
        const index = this.pendingRequests.findIndex(
          (r) => r.resolve === wrappedResolve
        )
        if (index !== -1) {
          this.pendingRequests.splice(index, 1)
        }
        reject(new Error(`Failed to send command: ${error.message}`))
      }
    })
  }

  /**
   * Terminate the session
   */
  terminate() {
    if (this.pythonProcess) {
      this.isActive = false
      this.pythonProcess.kill()
      this.pythonProcess = null
    }
  }

  /**
   * Check if session is idle
   */
  isIdle(maxIdleTime = 300000) {
    // 5 minutes default
    return Date.now() - this.lastActivity > maxIdleTime
  }
}

class SessionManager {
  constructor() {
    this.sessions = new Map()
    this.cleanupInterval = setInterval(() => this.cleanup(), 60000) // Cleanup every minute
  }

  /**
   * Create a new session
   */
  async createSession() {
    const sessionId = randomUUID()
    const session = new DiagnosisSession(sessionId)

    try {
      const result = await session.start()
      this.sessions.set(sessionId, session)
      return { sessionId, result }
    } catch (error) {
      session.terminate()
      throw error
    }
  }

  /**
   * Get an existing session
   */
  getSession(sessionId) {
    return this.sessions.get(sessionId)
  }

  /**
   * Send command to a session
   */
  async sendCommand(sessionId, command) {
    const session = this.getSession(sessionId)
    if (!session) {
      throw new Error('Session not found')
    }
    return session.sendCommand(command)
  }

  /**
   * Terminate a session
   */
  terminateSession(sessionId) {
    const session = this.sessions.get(sessionId)
    if (session) {
      session.terminate()
      this.sessions.delete(sessionId)
    }
  }

  /**
   * Cleanup idle sessions
   */
  cleanup() {
    const now = Date.now()
    for (const [sessionId, session] of this.sessions.entries()) {
      if (session.isIdle()) {
        console.log(`Cleaning up idle session: ${sessionId}`)
        session.terminate()
        this.sessions.delete(sessionId)
      }
    }
  }

  /**
   * Shutdown all sessions
   */
  shutdown() {
    clearInterval(this.cleanupInterval)
    for (const session of this.sessions.values()) {
      session.terminate()
    }
    this.sessions.clear()
  }
}

// Create singleton instance
const sessionManager = new SessionManager()

// Cleanup on process exit
process.on('SIGINT', () => {
  sessionManager.shutdown()
  process.exit(0)
})

process.on('SIGTERM', () => {
  sessionManager.shutdown()
  process.exit(0)
})

export default sessionManager
