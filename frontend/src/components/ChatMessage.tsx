import React from 'react'
import { cn } from '@/lib/utils'
import { Card } from '@/components/ui/card'
import type { ChatMessage as ChatMessageType } from '@/store/diagnosisStore'

interface ChatMessageProps {
  message: ChatMessageType
}

export const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isUser = message.sender === 'user'

  return (
    <div
      className={cn(
        'flex w-full mb-4 opacity-0 animate-[fadeIn_0.5s_ease-out_forwards]',
        isUser ? 'justify-end' : 'justify-start'
      )}
    >
      <div
        className={cn(
          'max-w-[80%] flex flex-col',
          isUser ? 'items-end' : 'items-start'
        )}
      >
        <Card
          className={cn(
            'px-4 py-3 shadow-md transition-all duration-200 hover:shadow-lg',
            isUser
              ? 'bg-primary text-primary-foreground rounded-br-none'
              : 'bg-card text-card-foreground rounded-bl-none border-border'
          )}
        >
          <p className="text-sm md:text-base leading-relaxed whitespace-pre-wrap">
            {message.content}
          </p>
        </Card>
        <span className="text-[10px] text-muted-foreground mt-1 px-1">
          {new Date(message.timestamp).toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit',
          })}
        </span>
      </div>
    </div>
  )
}
