import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Berkeley AI 25',
  description: 'Berkeley AI Hackathon 2025 Project',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}