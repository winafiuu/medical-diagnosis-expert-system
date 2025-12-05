import React from 'react'
import { AlertTriangle } from 'lucide-react'
import { cn } from '@/lib/utils'

interface DisclaimerBannerProps {
  className?: string
}

export const DisclaimerBanner: React.FC<DisclaimerBannerProps> = ({
  className,
}) => {
  return (
    <div
      className={cn(
        'bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-900/50 rounded-lg p-4 flex items-start gap-3 text-amber-800 dark:text-amber-200 shadow-sm',
        className
      )}
    >
      <AlertTriangle className="h-5 w-5 mt-0.5 shrink-0" />
      <div className="text-sm">
        <h4 className="font-semibold mb-1">Medical Disclaimer</h4>
        <p className="opacity-90 leading-relaxed">
          This AI system is for educational and experimental purposes only. It
          is <strong>not</strong> a substitute for professional medical advice,
          diagnosis, or treatment. Always seek the advice of your physician or
          other qualified health provider with any questions you may have
          regarding a medical condition.
        </p>
      </div>
    </div>
  )
}
