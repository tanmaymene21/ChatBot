import { useState, useRef, useEffect } from 'react';
import { useChat } from '../context/ChatContext';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../utils/axios';
import ChatMessage from './ChatMessage';

export default function Chat() {
  const { chatId } = useParams();
  const navigate = useNavigate();
  const [input, setInput] = useState('');
  const { state, dispatch } = useChat();
  const { messages, isLoading, currentChatId } = state;
  const messagesEndRef = useRef(null);

  useEffect(() => {
    if (chatId) {
      loadChat(chatId);
    }
  }, [chatId]);

  useEffect(() => {
    scrollToBottom();
  }, [messages.length]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  async function loadChat(chatId) {
    try {
      const response = await api.get(`/chatbot/chat/${chatId}`);
      const messages = response.data
        .map((msg) => [
          {
            type: 'user',
            content: msg.user_message,
            timestamp: new Date(msg.timestamp),
          },
          {
            type: 'bot',
            content: msg.bot_response,
            timestamp: new Date(msg.timestamp),
          },
        ])
        .flat();

      dispatch({
        type: 'LOAD_CHAT',
        payload: { messages, chatId },
      });
    } catch (error) {
      console.error('Failed to load chat:', error);
      if (error.response?.status !== 401) {
        navigate('/chat');
      }
    }
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const message = input.trim();
    setInput('');

    dispatch({ type: 'SEND_MESSAGE', payload: message });

    try {
      const response = await api.post('/chatbot/chat', {
        message,
        chat_id: currentChatId,
      });

      dispatch({
        type: 'RECEIVE_MESSAGE',
        payload: response.data.response,
        chatId: response.data.chat_id,
      });

      if (!currentChatId) {
        navigate(`/chat/${response.data.chat_id}`, { replace: true });
      }
    } catch (error) {
      dispatch({
        type: 'SET_ERROR',
        payload: 'Sorry, I encountered an error. Please try again.',
      });
    }
  }

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)] bg-white rounded-xl shadow-sm border border-gray-200">
      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-6">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-center px-4">
            <div className="rounded-full bg-blue-100 p-3 mb-4">
              <svg
                className="w-6 h-6 text-blue-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
                />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Welcome to AI Product Assistant
            </h3>
            <p className="text-gray-500 max-w-sm">
              Ask me anything about our products and suppliers. Try questions
              like "Which suppliers offer gaming
              accessories?"
            </p>
          </div>
        )}

        {messages.map((message, index) => (
          <ChatMessage key={index} message={message} />
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center mr-2">
              <div className="w-4 h-4 relative">
                <div className="animate-spin absolute w-full h-full border-2 border-blue-600 border-t-transparent rounded-full" />
              </div>
            </div>
            <div className="bg-white border border-gray-200 rounded-2xl px-6 py-4 shadow-sm">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:0.2s]" />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:0.4s]" />
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form
        onSubmit={handleSubmit}
        className="p-4 border-t border-gray-200 bg-gray-50"
      >
        <div className="flex space-x-4 max-w-4xl mx-auto">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about products or suppliers..."
            className="flex-1 rounded-xl border border-gray-300 px-4 py-3 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-shadow duration-200"
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="px-6 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200 font-medium flex items-center"
          >
            {isLoading ? (
              <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                  fill="none"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                />
              </svg>
            ) : (
              'Send'
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
