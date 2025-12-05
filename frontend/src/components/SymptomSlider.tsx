import React, { useEffect, useState } from 'react'
import { Slider } from '@/components/ui/slider'
import { cn } from '@/lib/utils'
import { Card } from '@/components/ui/card'

interface SymptomSliderProps {
  value: number
  onChange: (value: number) => void
  className?: string
}

export const SymptomSlider: React.FC<SymptomSliderProps> = ({
  value,
  onChange,
  className,
}) => {
  const [localValue, setLocalValue] = useState([value])

  useEffect(() => {
    setLocalValue([value])
  }, [value])

  const handleChange = (vals: number[]) => {
    setLocalValue(vals)
    onChange(vals[0])
  }

  const getLabel = (val: number) => {
    if (val < 20) return 'Very Unlikely'
    if (val < 40) return 'Unlikely'
    if (val < 60) return 'Possible'
    if (val < 80) return 'Likely'
    return 'Very Likely'
  }

  const label = getLabel(localValue[0])

  return (
    <Card className={cn('p-4 w-full max-w-md mx-auto space-y-4', className)}>
      <div className="flex justify-between items-center">
        <span className="text-sm font-medium text-foreground">
          Certainty Level
        </span>
        <span
          className={cn(
            'text-sm font-bold transition-colors duration-300',
            localValue[0] > 75 ? 'text-primary' : 'text-muted-foreground'
          )}
        >
          {localValue[0]}% - {label}
        </span>
      </div>
      <Slider
        value={localValue}
        onValueChange={handleChange}
        max={100}
        step={1}
        className="w-full cursor-pointer py-2"
        aria-label="Certainty slider"
      />
      <div className="flex justify-between text-xs text-muted-foreground px-1">
        <span>0%</span>
        <span>50%</span>
        <span>100%</span>
      </div>
    </Card>
  )
}
