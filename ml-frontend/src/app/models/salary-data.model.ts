export interface SalaryRecord {
  years: number;
  salary: number;
}

export interface SalaryDataResponse {
  records: SalaryRecord[];
  page: number;
  limit: number;
  totalRecords: number;
  totalPages: number;
}