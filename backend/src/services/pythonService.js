import { spawn } from 'child_process'
import path from 'path'
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

/**
 * Run the Python diagnosis engine with given input
 * @param {Object} input - Input data to send to Python engine
 * @returns {Promise<Object>} - Response from Python engine
 */
export const runDiagnosisEngine = (input) => {
  return new Promise((resolve, reject) => {
    const pythonPath =
      process.env.PYTHON_ENGINE_PATH ||
      path.join(__dirname, '../../../ai-engine/main.py')

    // Spawn Python process
    const pythonProcess = spawn('python3', [pythonPath])

    let outputData = ''
    let errorData = ''

    // Set timeout for Python process
    const timeout = setTimeout(() => {
      pythonProcess.kill()
      reject(new Error('Python process timeout'))
    }, 10000) // 10 second timeout

    // Collect stdout data
    pythonProcess.stdout.on('data', (data) => {
      outputData += data.toString()
    })

    // Collect stderr data
    pythonProcess.stderr.on('data', (data) => {
      errorData += data.toString()
    })

    // Handle process completion
    pythonProcess.on('close', (code) => {
      clearTimeout(timeout)

      if (code !== 0) {
        reject(
          new Error(`Python process exited with code ${code}: ${errorData}`)
        )
        return
      }

      try {
        const result = JSON.parse(outputData)
        resolve(result)
      } catch (error) {
        reject(
          new Error(
            `Failed to parse Python output: ${error.message}\nOutput: ${outputData}`
          )
        )
      }
    })

    // Handle process errors
    pythonProcess.on('error', (error) => {
      clearTimeout(timeout)
      reject(new Error(`Failed to start Python process: ${error.message}`))
    })

    // Send input to Python process
    pythonProcess.stdin.write(JSON.stringify(input))
    pythonProcess.stdin.end()
  })
}
