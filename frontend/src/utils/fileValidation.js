export const ALLOWED_TYPES = [
  "text/csv",
  "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  "application/pdf"
];

export const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB

export function validateFile(file) {
  if (!file) return "Please select a file";

  if (!ALLOWED_TYPES.includes(file.type)) {
    return "Only CSV, XLSX, and PDF files are allowed";
  }

  if (file.size > MAX_FILE_SIZE) {
    return "File size must be less than 10MB";
  }

  return null;
}
