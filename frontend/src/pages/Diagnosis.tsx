import { useState } from 'react'
import { ChatContainer } from '@/components/ChatContainer'
import { ChatInput } from '@/components/ChatInput'
import type { ChatMessage, MessageRole } from '@/store/diagnosisStore'

export default function Diagnosis() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      sender: 'system' as MessageRole,
      content:
        'Hello! I am your AI Medical Diagnosis Assistant. I will ask you a series of questions to help assess your respiratory symptoms. To begin, please tell me vaguely what you are feeling, or just click buttons if I present them.',
      timestamp: Date.now(),
    },
  ])
  const [isLoading, setIsLoading] = useState(false)

  const handleSend = (text: string) => {
    // Optimistic update for UI demo
    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      sender: 'user' as MessageRole,
      content: text,
      timestamp: Date.now(),
    }
    setMessages((prev) => [...prev, userMsg])
    setIsLoading(true)

    // Fake response delay
    setTimeout(() => {
      setIsLoading(false)
      const botMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: 'system' as MessageRole,
        content:
          'Thank you. I am just a layout demo right now, but soon I will be connected to the expert system engine!',
        timestamp: Date.now(),
      }
      setMessages((prev) => [...prev, botMsg])
    }, 1000)
  }

  return (
    <div className="flex flex-col items-center w-full max-w-4xl mx-auto space-y-6">
      <div className="text-center space-y-2 mb-4">
        <h2 className="text-2xl font-bold tracking-tight text-slate-900">
          Diagnosis Session
        </h2>
        <p className="text-muted-foreground">
          Answer the questions truthfully for the best results.
        </p>
      </div>

      <ChatContainer messages={messages} isLoading={isLoading}>
        <ChatInput onSend={handleSend} disabled={isLoading} />
      </ChatContainer>
    </div>
  )
}
