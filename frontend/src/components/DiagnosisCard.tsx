import React from 'react'
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
  CardDescription,
} from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { ConfidenceBar } from './ConfidenceBar'
import { DisclaimerBanner } from './DisclaimerBanner'
import { RefreshCcw } from 'lucide-react'

interface DiagnosisResult {
  disease: string
  description?: string
  confidence: number // 0-1
  explanation?: string
}

interface DiagnosisCardProps {
  result: DiagnosisResult | null
  onRestart?: () => void
  isLoading?: boolean
}

export const DiagnosisCard: React.FC<DiagnosisCardProps> = ({
  result,
  onRestart,
  isLoading,
}) => {
  if (!result && !isLoading) return null

  if (isLoading) {
    return (
      <Card className="w-full max-w-2xl mx-auto border-t-4 border-t-muted animate-pulse">
        <CardHeader className="space-y-2">
          <div className="h-6 w-1/3 bg-muted rounded"></div>
          <div className="h-4 w-1/2 bg-muted rounded"></div>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="h-32 bg-muted rounded-xl"></div>
          <div className="h-4 w-full bg-muted rounded"></div>
        </CardContent>
      </Card>
    )
  }

  // Safety check, though TypeScript should prevent this if used correctly
  if (!result) return null

  return (
    <div className="w-full max-w-2xl mx-auto space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <Card className="border-t-4 border-t-primary shadow-xl overflow-hidden bg-linear-to-b from-background to-muted/20">
        <CardHeader className="border-b pb-6 bg-muted/10">
          <CardTitle className="text-2xl lg:text-3xl text-center flex items-center justify-center gap-2">
            Diagnosis Result
          </CardTitle>
          <CardDescription className="text-center text-base mt-2">
            Based on the symptoms you reported
          </CardDescription>
        </CardHeader>

        <CardContent className="space-y-8 pt-6">
          {/* Main Result */}
          <div className="bg-background rounded-xl border shadow-sm p-8 text-center relative overflow-hidden">
            <div className="absolute top-0 left-0 w-full h-1 bg-linear-to-r from-transparent via-primary to-transparent opacity-50"></div>
            <h2 className="text-3xl lg:text-4xl font-bold text-primary mb-3">
              {result.disease}
            </h2>
            {result.description && (
              <p className="text-muted-foreground text-lg">
                {result.description}
              </p>
            )}
            {result.explanation && (
              <div className="mt-4 p-4 bg-muted/30 rounded-lg text-left text-sm text-muted-foreground">
                <p className="font-semibold mb-1">Analysis:</p>
                {result.explanation}
              </div>
            )}
          </div>

          {/* Confidence */}
          <div className="space-y-3 bg-muted/10 p-4 rounded-lg border">
            <h3 className="font-semibold text-lg flex justify-between">
              <span>Confidence Level</span>
            </h3>
            <ConfidenceBar
              confidence={result.confidence}
              label="Match Probability"
            />
            <p className="text-xs text-muted-foreground mt-2">
              This percentage indicates how closely your symptoms match known
              patterns for this condition.
            </p>
          </div>
        </CardContent>

        <CardFooter className="flex flex-col gap-4 bg-muted/20 p-6 border-t">
          <DisclaimerBanner />

          {onRestart && (
            <div className="pt-2 w-full flex justify-center">
              <Button
                onClick={onRestart}
                size="lg"
                className="w-full sm:w-auto font-semibold gap-2 shadow-md hover:shadow-lg transition-all"
              >
                <RefreshCcw className="h-4 w-4" />
                Start New Diagnosis
              </Button>
            </div>
          )}
        </CardFooter>
      </Card>
    </div>
  )
}
