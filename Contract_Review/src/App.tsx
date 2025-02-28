import React, { useState } from 'react';
import { Upload, AlertTriangle, CheckCircle, FileText } from 'lucide-react';

interface RiskClause {
  type: string;
  score: number;
  suggestion: string;
}

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [results, setResults] = useState<RiskClause[]>([]);

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const uploadedFile = event.target.files?.[0];
    if (uploadedFile) {
      setFile(uploadedFile);
      // Simulate analysis
      setAnalyzing(true);
      setTimeout(() => {
        setAnalyzing(false);
        setResults([
          {
            type: "termination without cause",
            score: 0.85,
            suggestion: "Consider requiring prior notice and valid justification."
          },
          {
            type: "non-compete clause",
            score: 0.76,
            suggestion: "Limit non-compete clauses to a reasonable time and geographic scope."
          },
          {
            type: "data privacy violations",
            score: 0.62,
            suggestion: "Ensure compliance with GDPR by defining data retention policies."
          }
        ]);
      }, 2000);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              AI-Powered Contract Review
            </h1>
            <p className="text-lg text-gray-600">
              Upload your contract document for instant risk analysis
            </p>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
              <input
                type="file"
                accept=".pdf,.docx"
                onChange={handleFileUpload}
                className="hidden"
                id="file-upload"
              />
              <label
                htmlFor="file-upload"
                className="cursor-pointer inline-flex flex-col items-center"
              >
                <Upload className="w-12 h-12 text-blue-500 mb-4" />
                <span className="text-lg font-medium text-gray-700">
                  {file ? file.name : "Drop your contract here or click to upload"}
                </span>
                <span className="text-sm text-gray-500 mt-2">
                  Supports PDF and DOCX files
                </span>
              </label>
            </div>
          </div>

          {analyzing && (
            <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
              <div className="flex items-center justify-center">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mr-3"></div>
                <span className="text-lg text-gray-700">Analyzing contract...</span>
              </div>
            </div>
          )}

          {results.length > 0 && (
            <div className="bg-white rounded-xl shadow-lg p-8">
              <h2 className="text-2xl font-semibold text-gray-900 mb-6">Analysis Results</h2>
              
              <div className="space-y-6">
                {results.map((result, index) => (
                  <div key={index} className="border-l-4 border-yellow-400 bg-yellow-50 p-6 rounded-r-lg">
                    <div className="flex items-start">
                      <AlertTriangle className="w-6 h-6 text-yellow-500 mr-4 flex-shrink-0 mt-1" />
                      <div>
                        <h3 className="text-lg font-medium text-gray-900 capitalize">
                          {result.type}
                        </h3>
                        <p className="text-sm text-gray-600 mt-1">
                          Risk Score: {(result.score * 100).toFixed(0)}%
                        </p>
                        <div className="mt-3 bg-white p-4 rounded-lg border border-yellow-200">
                          <p className="text-sm text-gray-700">
                            <span className="font-medium">Suggestion: </span>
                            {result.suggestion}
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;