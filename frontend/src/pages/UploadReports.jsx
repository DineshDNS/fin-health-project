import FileUpload from "../components/FileUpload";

function UploadReports() {
  return (
    <div style={{ padding: "20px" }}>
      <h2>Upload Financial Documents</h2>
      <ul>
        <li>Profit & Loss Reports</li>
        <li>Balance Sheets</li>
        <li>Cash Flow Statements</li>
        <li>Bank / Accounting Exports</li>
      </ul>
      <p>Supported formats: CSV, XLSX, PDF (text-based)</p>
      <FileUpload />
    </div>
  );
}

export default UploadReports;
