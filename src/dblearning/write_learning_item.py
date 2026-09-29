filepath = 'D:/DemoCN2026/dblearning/frontend/src/pages/LearningItem.jsx'
content = '''import { useEffect, useState } from 'react';
import { learningApi } from '../api/learningApi';
import { useParams, Link } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';

export default function LearningItem() {
  const { itemId } = useParams();
  const [item, setItem] = useState(null);
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchItem = async () => {
      try {
        const data = await learningApi.getLearningItem(itemId);
        setItem(data);
        
        // Start learning session automatically
        const sess = await learningApi.startSession(itemId);
        setSession(sess);
      } catch (err) {
        console.error("Error fetching item", err);
      } finally {
        setLoading(false);
      }
    };
    fetchItem();
  }, [itemId]);

  const handleFinish = async () => {
    if (session) {
      await learningApi.endSession(session.id);
    }
  };

  if (loading) return <div className="p-8 text-center text-gray-500">Đang tải nội dung...</div>;
  if (!item) return <div className="p-8 text-center text-red-500">Không tìm thấy bài học</div>;

  return (
    <div className="max-w-4xl mx-auto pt-6 pb-12">
      <Link to={"/topics/" + item.topic_id} className="text-primary-600 hover:underline mb-4 inline-block">&larr; Quay lại danh sách</Link>
      
      <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-8 md:p-12">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 pb-6 border-b border-gray-100">
          <h1 className="text-3xl font-bold text-gray-900 mb-4 md:mb-0">{item.title}</h1>
          <span className="text-sm px-4 py-1.5 bg-blue-50 text-blue-700 rounded-full font-medium whitespace-nowrap">
            {item.content_type === 'document' ? 'Lý thuyết' : 'Thực hành'}
          </span>
        </div>
        
        <div className="prose prose-lg prose-blue max-w-none text-gray-700 mb-10">
          {item.content_body ? (
             <ReactMarkdown>{item.content_body}</ReactMarkdown>
          ) : (
            <div className="bg-gray-50 p-8 rounded-xl border border-gray-100 flex flex-col items-center justify-center min-h-[200px]">
              <p className="text-gray-500">Nội dung bài học đang được biên soạn.</p>
            </div>
          )}
        </div>
        
        {/* Nguồn tham khảo (Tài liệu gốc) */}
        {item.content_url && (
          <div className="bg-blue-50/50 border border-blue-100 rounded-xl p-6 mb-10">
            <div className="flex items-start">
              <div className="flex-shrink-0 mt-1">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <div className="ml-4 flex-1">
                <h3 className="text-lg font-bold text-gray-900 mb-1">Tài liệu tham khảo chuyên sâu</h3>
                <p className="text-gray-600 mb-4 text-sm">
                  Bạn muốn tìm hiểu cặn kẽ và chuyên sâu hơn? Dưới đây là tài liệu PDF gốc được cung cấp cho bài học này.
                </p>
                <a 
                  href={"http://localhost:8000" + item.content_url} 
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center justify-center bg-white border border-gray-300 text-gray-700 px-5 py-2.5 rounded-lg font-medium hover:bg-gray-50 hover:text-blue-600 transition-colors shadow-sm"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                  </svg>
                  Tải/Xem tài liệu gốc
                </a>
              </div>
            </div>
          </div>
        )}
        
        <div className="pt-6 border-t border-gray-100 flex justify-end">
          <Link 
            to={"/topics/" + item.topic_id} 
            onClick={handleFinish}
            className="bg-primary-600 text-white px-8 py-3 rounded-xl font-semibold hover:bg-primary-700 transition-colors shadow-sm shadow-primary-600/30"
          >
            Hoàn thành bài học &rarr;
          </Link>
        </div>
      </div>
    </div>
  );
}
'''

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
