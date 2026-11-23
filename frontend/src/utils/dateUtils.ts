/**
 * Time and ID generation utilities for SahyogSetu
 */

export function getCurrentTime(): string {
  return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

export function getFormattedDate(ms?: number): string {
  const time = ms ?? Date.now();
  return new Date(time).toLocaleDateString([], {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

export function generateMessageId(type: 'user' | 'asst' | 'err' | 'resp'): string {
  return `msg_${type}_${Date.now()}_${Math.random().toString(36).slice(2, 6)}`;
}

export function generateConversationId(): string {
  return `conv_${Date.now()}_${Math.random().toString(36).slice(2, 6)}`;
}
