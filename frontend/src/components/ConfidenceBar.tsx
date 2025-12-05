import React from 'react'
import { cn } from '@/lib/utils'

interface ConfidenceBarProps {
  confidence: number // 0 to 1
  label?: string
  className?: string
  showPercentage?: boolean
}

export const ConfidenceBar: React.FC<ConfidenceBarProps> = ({
  confidence,
  label,
  className,
  showPercentage = true,
}) => {
  // Clamp between 0 and 100
  const percentage = Math.min(Math.max(confidence * 100, 0), 100)

  // Determine color based on confidence level
  // < 50: Yellow/Orange (Low)
  // 50 - 80: Blue/Cyan (Medium)
  // > 80: Green (High)
  let colorClass = 'bg-yellow-500'
  if (percentage >= 80) colorClass = 'bg-green-500'
  else if (percentage >= 50) colorClass = 'bg-blue-500'

  return (
    <div className={cn('w-full space-y-2', className)}>
      <div className="flex justify-between items-center text-sm">
        {label && <span className="font-medium text-foreground">{label}</span>}
        {showPercentage && (
          <span className="font-bold text-muted-foreground">
            {percentage.toFixed(1)}%
          </span>
        )}
      </div>
      <div className="h-3 w-full bg-secondary rounded-full overflow-hidden">
        <div
          className={cn(
            'h-full transition-all duration-1000 ease-out rounded-full shadow-sm',
            colorClass
          )}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  )
}
