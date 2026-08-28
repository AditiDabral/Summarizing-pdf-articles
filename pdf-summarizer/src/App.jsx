import { useState } from "react";
import { Upload, FileText, Sparkles, X } from "lucide-react";

function App() {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);

  // When user selects a PDF
  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];

    if (!selectedFile) {
      return;
    }

    if (selectedFile.type !== "application/pdf") {
      alert("Please select a PDF file.");
      return;
    }

    setFile(selectedFile);
    setSummary("");
  };

  // Remove selected PDF
  const removeFile = () => {
    setFile(null);
    setSummary("");
  };

  // Send test text to backend
  const handleSummarize = async () => {
    if (!file) {
      alert("Please upload a PDF first.");
      return;
    }

    setLoading(true);
    setSummary("");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/summarize",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            text: "Artificial intelligence is a technology that allows computers to perform tasks that normally require human intelligence. Machine learning is a part of artificial intelligence where computers learn patterns from data. AI is used in healthcare, education, finance, transportation and many other industries.",
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Backend request failed");
      }

      const data = await response.json();

      setSummary(data.summary);
    } catch (error) {
      console.error("Error:", error);

      setSummary(
        "Could not connect to the backend. Please make sure your friend's FastAPI server is running."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#f8fafc] text-slate-900">

      {/* Navbar */}
      <nav className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">

          <div className="flex items-center gap-3">

            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-slate-900">
              <Sparkles size={18} className="text-white" />
            </div>

            <span className="text-lg font-semibold tracking-tight">
              SummarAI
            </span>

          </div>

          <span className="hidden text-sm text-slate-500 sm:block">
            AI PDF Summarizer
          </span>

        </div>
      </nav>


      {/* Main */}
      <main className="mx-auto max-w-3xl px-6 py-16">

        {/* Hero */}
        <div className="mb-10 text-center">

          <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-4 py-2 text-sm text-slate-600 shadow-sm">
            <Sparkles size={15} />
            AI-powered summarization
          </div>

          <h1 className="text-4xl font-bold tracking-tight sm:text-5xl">
            Understand your PDFs
            <span className="block text-slate-400">
              in seconds.
            </span>
          </h1>

          <p className="mx-auto mt-5 max-w-xl text-base leading-7 text-slate-500">
            Upload a PDF and let AI extract the most important
            information for you.
          </p>

        </div>


        {/* Upload Card */}
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">

          {!file ? (

            <label
              htmlFor="pdf-upload"
              className="group flex cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed border-slate-200 bg-slate-50 px-6 py-14 transition hover:border-slate-400 hover:bg-slate-100"
            >

              <div className="mb-5 flex h-16 w-16 items-center justify-center rounded-2xl bg-white shadow-sm ring-1 ring-slate-200 transition group-hover:scale-105">
                <Upload
                  size={25}
                  className="text-slate-600"
                />
              </div>

              <h2 className="text-base font-semibold">
                Upload your PDF
              </h2>

              <p className="mt-2 text-sm text-slate-500">
                Drag and drop your file here, or{" "}
                <span className="font-medium text-slate-900 underline underline-offset-2">
                  browse
                </span>
              </p>

              <p className="mt-4 text-xs text-slate-400">
                PDF files only
              </p>

              <input
                id="pdf-upload"
                type="file"
                accept="application/pdf"
                onChange={handleFileChange}
                className="hidden"
              />

            </label>

          ) : (

            /* Selected File */
            <div className="rounded-xl border border-slate-200 bg-slate-50 p-4">

              <div className="flex items-center justify-between">

                <div className="flex min-w-0 items-center gap-4">

                  <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-white shadow-sm ring-1 ring-slate-200">
                    <FileText
                      size={21}
                      className="text-slate-600"
                    />
                  </div>

                  <div className="min-w-0">

                    <p className="truncate text-sm font-semibold text-slate-800">
                      {file.name}
                    </p>

                    <p className="mt-1 text-xs text-slate-500">
                      {(file.size / 1024 / 1024).toFixed(2)} MB
                    </p>

                  </div>

                </div>

                <button
                  onClick={removeFile}
                  className="ml-3 rounded-lg p-2 text-slate-400 transition hover:bg-white hover:text-slate-700"
                >
                  <X size={18} />
                </button>

              </div>

            </div>
          )}


          {/* Summarize Button */}
          <button
            onClick={handleSummarize}
            disabled={loading}
            className="mt-5 flex w-full items-center justify-center gap-2 rounded-xl bg-slate-900 px-5 py-3.5 text-sm font-semibold text-white shadow-sm transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60"
          >

            <Sparkles size={17} />

            {loading ? "Summarizing..." : "Summarize PDF"}

          </button>

        </div>


        {/* Summary */}
        {summary && (

          <div className="mt-6 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">

            <div className="mb-5 flex items-center gap-3">

              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-slate-100">
                <Sparkles size={18} />
              </div>

              <div>

                <h2 className="font-semibold">
                  Summary
                </h2>

                <p className="text-xs text-slate-400">
                  AI-generated overview
                </p>

              </div>

            </div>


            <div className="rounded-xl bg-slate-50 p-5">

              <p className="text-sm leading-7 text-slate-600">
                {summary}
              </p>

            </div>

          </div>

        )}


        {/* Footer */}
        <p className="mt-8 text-center text-xs text-slate-400">
          Your PDF will be processed by the backend.
        </p>

      </main>

    </div>
  );
}

export default App;