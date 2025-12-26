import '../../styles/globals.css';

export const metadata = {
  title: 'Dark Mode Todo App',
  description: 'A sleek dark-themed full-stack Next.js todo application with database persistence',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  )
}
