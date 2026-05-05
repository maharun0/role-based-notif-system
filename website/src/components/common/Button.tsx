interface ButtonProps {
  children: React.ReactNode
  onClick?: () => void
  variant?: 'primary' | 'secondary' | 'ghost'
  disabled?: boolean
  type?: 'button' | 'submit'
  className?: string
}

const VARIANTS = {
  primary: 'bg-blue-600 text-white hover:bg-blue-700 disabled:bg-blue-300',
  secondary: 'bg-gray-100 text-gray-700 hover:bg-gray-200 disabled:bg-gray-100 disabled:text-gray-400',
  ghost: 'text-gray-500 hover:text-gray-700 hover:bg-gray-100',
}

export default function Button({
  children,
  onClick,
  variant = 'primary',
  disabled = false,
  type = 'button',
  className = '',
}: ButtonProps) {
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md text-sm font-medium transition-colors cursor-pointer disabled:cursor-not-allowed ${VARIANTS[variant]} ${className}`}
    >
      {children}
    </button>
  )
}
