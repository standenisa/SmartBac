import { createContext, useContext, useState, useCallback, useRef, ReactNode } from 'react';
import Toast, { ToastData } from '@/components/Toast';

interface ToastContextValue {
  showToast: (data: ToastData) => void;
}

const ToastContext = createContext<ToastContextValue>({ showToast: () => {} });

export function useToast() {
  return useContext(ToastContext);
}

export function ToastProvider({ children }: { children: ReactNode }) {
  const [toast, setToast] = useState<ToastData | null>(null);
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const dismiss = useCallback(() => {
    setToast(null);
    if (timerRef.current) clearTimeout(timerRef.current);
  }, []);

  const showToast = useCallback((data: ToastData) => {
    if (timerRef.current) clearTimeout(timerRef.current);
    setToast(data);
    timerRef.current = setTimeout(dismiss, 3000);
  }, [dismiss]);

  return (
    <ToastContext.Provider value={{ showToast }}>
      {children}
      {toast && <Toast data={toast} onDismiss={dismiss} />}
    </ToastContext.Provider>
  );
}
