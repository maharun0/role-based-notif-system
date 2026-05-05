interface BadgeProps {
  count: number
}

export default function Badge({ count }: BadgeProps) {
  if (count === 0) return null
  return (
    <span className="absolute -top-1 -right-1 min-w-[18px] h-[18px] bg-red-500 text-white text-[10px] font-bold rounded-full flex items-center justify-center px-1 leading-none">
      {count > 99 ? '99+' : count}
    </span>
  )
}
