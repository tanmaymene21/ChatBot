import { createContext, useContext, useReducer } from 'react';

const ChatContext = createContext();

const initialState = {
  messages: [],
  isLoading: false,
  error: null,
  currentChatId: null,
  lastMessageTimestamp: null,
};

function chatReducer(state, action) {
  switch (action.type) {
    case 'SEND_MESSAGE':
      return {
        ...state,
        messages: [
          ...state.messages,
          { type: 'user', content: action.payload },
        ],
        isLoading: true,
        lastMessageTimestamp: Date.now(),
      };
    case 'RECEIVE_MESSAGE':
      return {
        ...state,
        messages: [...state.messages, { type: 'bot', content: action.payload }],
        isLoading: false,
        currentChatId: action.chatId || state.currentChatId,
        lastMessageTimestamp: Date.now(),
      };
    case 'SET_ERROR':
      return {
        ...state,
        error: action.payload,
        isLoading: false,
      };
    case 'CLEAR_MESSAGES':
      return {
        ...state,
        messages: [],
        currentChatId: null,
      };
    case 'LOAD_CHAT':
      return {
        ...state,
        messages: action.payload.messages,
        currentChatId: action.payload.chatId,
        isLoading: false,
      };
    default:
      return state;
  }
}

export function ChatProvider({ children }) {
  const [state, dispatch] = useReducer(chatReducer, initialState);

  return (
    <ChatContext.Provider value={{ state, dispatch }}>
      {children}
    </ChatContext.Provider>
  );
}

export function useChat() {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
}
