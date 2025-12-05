import React from 'react'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'
import { Check, X, HelpCircle } from 'lucide-react'

interface QuickResponseButtonsProps {
  onSelect: (value: string, cf?: number) => void
  className?: string
  disabled?: boolean
}

export const QuickResponseButtons: React.FC<QuickResponseButtonsProps> = ({
  onSelect,
  className,
  disabled = false,
}) => {
  return (
    <div
      className={cn(
        'flex flex-wrap gap-2 justify-center w-full my-2',
        className
      )}
    >
      <Button
        variant="outline"
        size="lg"
        onClick={() => onSelect('yes', 100)}
        disabled={disabled}
        className="flex-1 min-w-[100px] border-green-200 hover:bg-green-50 hover:text-green-700 hover:border-green-300 dark:border-green-900 dark:hover:bg-green-950 dark:hover:text-green-400 transition-all"
      >
        <Check className="mr-2 h-4 w-4" />
        Yes
      </Button>

      <Button
        variant="outline"
        size="lg"
        onClick={() => onSelect('no', 0)}
        // Assuming 'no' means 0% certainty of the symptom or just negative response.
        // If the backend expects low CF for 'no', we might send 0 or -100 depending on logic.
        // For now, let's just pass 'no'. Sender can handle logic.
        disabled={disabled}
        className="flex-1 min-w-[100px] border-red-200 hover:bg-red-50 hover:text-red-700 hover:border-red-300 dark:border-red-900 dark:hover:bg-red-950 dark:hover:text-red-400 transition-all"
      >
        <X className="mr-2 h-4 w-4" />
        No
      </Button>

      <Button
        variant="outline"
        size="lg"
        onClick={() => onSelect('unsure', 50)}
        disabled={disabled}
        className="flex-1 min-w-[100px] border-yellow-200 hover:bg-yellow-50 hover:text-yellow-700 hover:border-yellow-300 dark:border-yellow-900 dark:hover:bg-yellow-950 dark:hover:text-yellow-400 transition-all"
      >
        <HelpCircle className="mr-2 h-4 w-4" />
        Unsure
      </Button>
    </div>
  )
}
