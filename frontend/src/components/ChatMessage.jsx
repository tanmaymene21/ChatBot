import { useMemo } from 'react';

function ProductCard({ product }) {
  return (
    <div className="bg-white rounded-lg border border-gray-200 p-4 hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start">
        <h4 className="text-lg font-medium text-gray-900">{product.name}</h4>
        <span className="px-2.5 py-1 bg-blue-100 text-blue-800 text-sm font-medium rounded-full">
          ${product.price}
        </span>
      </div>
      <p className="text-sm text-gray-600 mt-1">{product.brand}</p>
      <div className="mt-2">
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
          {product.category}
        </span>
      </div>
      <p className="mt-2 text-sm text-gray-500">{product.description}</p>
    </div>
  );
}

function SupplierCard({ supplier }) {
  return (
    <div className="bg-white rounded-lg border border-gray-200 p-4 hover:shadow-md transition-shadow">
      <h4 className="text-lg font-medium text-gray-900">{supplier.name}</h4>
      <p className="text-sm text-gray-600 mt-1">{supplier.contact}</p>
      <div className="mt-2 flex flex-wrap gap-2">
        {supplier.categories_offered.map((category, idx) => (
          <span
            key={idx}
            className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800"
          >
            {category}
          </span>
        ))}
      </div>
    </div>
  );
}

function formatResponse(content) {
  try {
    const data = JSON.parse(content);

    if (data.products) {
      return (
        <div className="space-y-4">
          <h3 className="text-lg font-medium text-gray-900 mb-3">
            Products ({data.products.length})
          </h3>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            {data.products.map((product, idx) => (
              <ProductCard key={idx} product={product} />
            ))}
          </div>
        </div>
      );
    }

    if (data.suppliers) {
      return (
        <div className="space-y-4">
          <h3 className="text-lg font-medium text-gray-900 mb-3">
            Suppliers ({data.suppliers.length})
          </h3>
          <div className="grid grid-cols-1 gap-4">
            {data.suppliers.map((supplier, idx) => (
              <SupplierCard key={idx} supplier={supplier} />
            ))}
          </div>
        </div>
      );
    }

    if (data.error) {
      return (
        <div className="rounded-lg bg-red-50 p-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg
                className="h-5 w-5 text-red-400"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                  clipRule="evenodd"
                />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-red-700">{data.error}</p>
            </div>
          </div>
        </div>
      );
    }
  } catch (e) {
    return <p className="text-gray-900 whitespace-pre-wrap">{content}</p>;
  }
}

export default function ChatMessage({ message }) {
  const formattedContent = useMemo(
    () => formatResponse(message.content),
    [message.content]
  );

  return (
    <div
      className={`flex ${
        message.type === 'user' ? 'justify-end' : 'justify-start'
      } animate-fade-in`}
    >
      {message.type === 'bot' && (
        <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center mr-2">
          <svg
            className="w-4 h-4 text-blue-600"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z"
            />
          </svg>
        </div>
      )}
      <div
        className={`max-w-[85%] rounded-2xl px-6 py-4 ${
          message.type === 'user'
            ? 'bg-blue-600 text-white ml-4'
            : 'bg-white border border-gray-200 shadow-sm'
        }`}
      >
        {message.type === 'user' ? (
          <p className="text-white">{message.content}</p>
        ) : (
          formattedContent
        )}
      </div>
      {message.type === 'user' && (
        <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center ml-2">
          <svg
            className="w-4 h-4 text-white"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
            />
          </svg>
        </div>
      )}
    </div>
  );
}
