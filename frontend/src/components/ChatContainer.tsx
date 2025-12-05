import React, { useRef, useEffect } from 'react'
import { ScrollArea } from '@/components/ui/scroll-area'
import { cn } from '@/lib/utils'
import { ChatMessage } from './ChatMessage'
import type { ChatMessage as ChatMessageType } from '@/store/diagnosisStore'

interface ChatContainerProps {
  messages: ChatMessageType[]
  isLoading?: boolean
  className?: string
  children?: React.ReactNode // For the input area or extra content
}

export const ChatContainer: React.FC<ChatContainerProps> = ({
  messages,
  isLoading = false,
  className,
  children,
}) => {
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // Auto-scroll to bottom when messages change
    if (bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }, [messages, isLoading])

  return (
    <div
      className={cn(
        'flex flex-col h-full w-full bg-background/50 border rounded-xl shadow-sm overflow-hidden',
        className
      )}
    >
      <div className="flex-1 overflow-hidden relative">
        <ScrollArea className="h-full w-full p-4">
          <div className="flex flex-col space-y-4 pb-4">
            {messages.length === 0 && (
              <div className="flex flex-col items-center justify-center h-full min-h-[200px] text-muted-foreground animate-in fade-in zoom-in duration-500">
                <p className="text-lg font-medium">
                  Medical Diagnosis Assistant
                </p>
                <p className="text-sm">
                  Start a new session to begin diagnosis.
                </p>
              </div>
            )}

            {messages.map((msg) => (
              <ChatMessage key={msg.id} message={msg} />
            ))}

            {isLoading && (
              <div className="flex justify-start w-full animate-pulse">
                <div className="bg-muted px-4 py-3 rounded-lg rounded-bl-none text-sm text-muted-foreground">
                  Thinking...
                </div>
              </div>
            )}
            <div ref={bottomRef} />
          </div>
        </ScrollArea>
      </div>

      {/* Input Area Footer - Only render if children exist */}
      {children && (
        <div className="p-4 bg-muted/30 border-t backdrop-blur-sm">
          {children}
        </div>
      )}
    </div>
  )
}
