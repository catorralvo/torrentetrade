export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export type Database = {
  __InternalSupabase: {
    PostgrestVersion: "14.17"
  }
  public: {
    Tables: {
      dont100_events: {
        Row: {
          client_event_id: string
          created_at: string
          event_type: string
          id: number
          level: number | null
          level_seed: number | null
          level_time_ms: number | null
          mechanic: string | null
          metadata: Json
          player_id: string
          run_id: string
          total_time_ms: number | null
          user_id: string | null
        }
        Insert: {
          client_event_id: string
          created_at?: string
          event_type: string
          id?: never
          level?: number | null
          level_seed?: number | null
          level_time_ms?: number | null
          mechanic?: string | null
          metadata?: Json
          player_id: string
          run_id: string
          total_time_ms?: number | null
          user_id?: string | null
        }
        Update: {
          client_event_id?: string
          created_at?: string
          event_type?: string
          id?: never
          level?: number | null
          level_seed?: number | null
          level_time_ms?: number | null
          mechanic?: string | null
          metadata?: Json
          player_id?: string
          run_id?: string
          total_time_ms?: number | null
          user_id?: string | null
        }
        Relationships: [{ foreignKeyName: "dont100_events_run_id_fkey"; columns: ["run_id"]; isOneToOne: false; referencedRelation: "dont100_runs"; referencedColumns: ["id"] }]
      }
      dont100_public_leaderboard: {
        Row: { build_version: string | null; country_code: string | null; created_at: string; finished_at: string; language: string; nickname: string | null; run_id: string; total_time_ms: number }
        Insert: { build_version?: string | null; country_code?: string | null; created_at?: string; finished_at: string; language: string; nickname?: string | null; run_id: string; total_time_ms: number }
        Update: { build_version?: string | null; country_code?: string | null; created_at?: string; finished_at?: string; language?: string; nickname?: string | null; run_id?: string; total_time_ms?: number }
        Relationships: [{ foreignKeyName: "dont100_public_leaderboard_run_id_fkey"; columns: ["run_id"]; isOneToOne: true; referencedRelation: "dont100_runs"; referencedColumns: ["id"] }]
      }
      dont100_runs: {
        Row: { build_version: string | null; checkpoint_restarts: number; completed: boolean; country_code: string | null; created_at: string; finished_at: string | null; highest_level: number; id: string; language: string; nickname: string | null; player_id: string; revives: number; run_seed: number | null; started_at: string; total_time_ms: number | null; user_id: string | null; verified: boolean }
        Insert: { build_version?: string | null; checkpoint_restarts?: number; completed?: boolean; country_code?: string | null; created_at?: string; finished_at?: string | null; highest_level?: number; id?: string; language?: string; nickname?: string | null; player_id: string; revives?: number; run_seed?: number | null; started_at?: string; total_time_ms?: number | null; user_id?: string | null; verified?: boolean }
        Update: { build_version?: string | null; checkpoint_restarts?: number; completed?: boolean; country_code?: string | null; created_at?: string; finished_at?: string | null; highest_level?: number; id?: string; language?: string; nickname?: string | null; player_id?: string; revives?: number; run_seed?: number | null; started_at?: string; total_time_ms?: number | null; user_id?: string | null; verified?: boolean }
        Relationships: []
      }
      subvench_alerts: {
        Row: { body: string; created_at: string; id: string; kind: string; payload: Json; program_id: string | null; project_id: string | null; read_at: string | null; title: string; user_id: string }
        Insert: { body: string; created_at?: string; id?: string; kind: string; payload?: Json; program_id?: string | null; project_id?: string | null; read_at?: string | null; title: string; user_id: string }
        Update: { body?: string; created_at?: string; id?: string; kind?: string; payload?: Json; program_id?: string | null; project_id?: string | null; read_at?: string | null; title?: string; user_id?: string }
        Relationships: [{ foreignKeyName: "subvench_alerts_project_id_fkey"; columns: ["project_id"]; isOneToOne: false; referencedRelation: "subvench_projects"; referencedColumns: ["id"] }]
      }
      subvench_profiles: {
        Row: { canton: string | null; company_name: string | null; created_at: string; fte: number | null; id: string; industrial_company: boolean | null; industry_hightech: boolean | null; is_startup: boolean | null; local_jobs_impact: boolean | null; market_established: boolean | null; production_tool_in_canton: boolean | null; rd_or_production_in_canton: boolean | null; swiss_uid: string | null; updated_at: string; user_id: string }
        Insert: { canton?: string | null; company_name?: string | null; created_at?: string; fte?: number | null; id?: string; industrial_company?: boolean | null; industry_hightech?: boolean | null; is_startup?: boolean | null; local_jobs_impact?: boolean | null; market_established?: boolean | null; production_tool_in_canton?: boolean | null; rd_or_production_in_canton?: boolean | null; swiss_uid?: string | null; updated_at?: string; user_id: string }
        Update: { canton?: string | null; company_name?: string | null; created_at?: string; fte?: number | null; id?: string; industrial_company?: boolean | null; industry_hightech?: boolean | null; is_startup?: boolean | null; local_jobs_impact?: boolean | null; market_established?: boolean | null; production_tool_in_canton?: boolean | null; rd_or_production_in_canton?: boolean | null; swiss_uid?: string | null; updated_at?: string; user_id?: string }
        Relationships: []
      }
      subvench_program_versions: {
        Row: { effective_from: string | null; effective_to: string | null; id: string; is_current: boolean; program_id: string; source_hash: string | null; source_url: string; structured_payload: Json; verified_at: string }
        Insert: { effective_from?: string | null; effective_to?: string | null; id?: string; is_current?: boolean; program_id: string; source_hash?: string | null; source_url: string; structured_payload: Json; verified_at?: string }
        Update: { effective_from?: string | null; effective_to?: string | null; id?: string; is_current?: boolean; program_id?: string; source_hash?: string | null; source_url?: string; structured_payload?: Json; verified_at?: string }
        Relationships: []
      }
      subvench_projects: {
        Row: { budget_chf: number | null; created_at: string; description: string; foreign_local_partner: boolean | null; geneva_research_partner: boolean | null; id: string; name: string; profile_id: string | null; project_started: boolean | null; status: string; swiss_research_partner: boolean | null; target_start_date: string | null; updated_at: string; user_id: string }
        Insert: { budget_chf?: number | null; created_at?: string; description?: string; foreign_local_partner?: boolean | null; geneva_research_partner?: boolean | null; id?: string; name: string; profile_id?: string | null; project_started?: boolean | null; status?: string; swiss_research_partner?: boolean | null; target_start_date?: string | null; updated_at?: string; user_id: string }
        Update: { budget_chf?: number | null; created_at?: string; description?: string; foreign_local_partner?: boolean | null; geneva_research_partner?: boolean | null; id?: string; name?: string; profile_id?: string | null; project_started?: boolean | null; status?: string; swiss_research_partner?: boolean | null; target_start_date?: string | null; updated_at?: string; user_id?: string }
        Relationships: [{ foreignKeyName: "subvench_projects_profile_id_fkey"; columns: ["profile_id"]; isOneToOne: false; referencedRelation: "subvench_profiles"; referencedColumns: ["id"] }]
      }
      subvench_scans: {
        Row: { catalog_version: string; created_at: string; engine_version: string; id: string; input_snapshot: Json; project_id: string; result_snapshot: Json; user_id: string }
        Insert: { catalog_version: string; created_at?: string; engine_version: string; id?: string; input_snapshot: Json; project_id: string; result_snapshot: Json; user_id: string }
        Update: { catalog_version?: string; created_at?: string; engine_version?: string; id?: string; input_snapshot?: Json; project_id?: string; result_snapshot?: Json; user_id?: string }
        Relationships: [{ foreignKeyName: "subvench_scans_project_id_fkey"; columns: ["project_id"]; isOneToOne: false; referencedRelation: "subvench_projects"; referencedColumns: ["id"] }]
      }
      subvench_watches: {
        Row: { created_at: string; enabled: boolean; id: string; last_change_at: string | null; last_checked_at: string | null; program_id: string | null; project_id: string; user_id: string; watch_type: string }
        Insert: { created_at?: string; enabled?: boolean; id?: string; last_change_at?: string | null; last_checked_at?: string | null; program_id?: string | null; project_id: string; user_id: string; watch_type?: string }
        Update: { created_at?: string; enabled?: boolean; id?: string; last_change_at?: string | null; last_checked_at?: string | null; program_id?: string | null; project_id?: string; user_id?: string; watch_type?: string }
        Relationships: [{ foreignKeyName: "subvench_watches_project_id_fkey"; columns: ["project_id"]; isOneToOne: false; referencedRelation: "subvench_projects"; referencedColumns: ["id"] }]
      }
    }
    Views: {
      dont100_leaderboard: {
        Row: { build_version: string | null; country_code: string | null; finished_at: string | null; id: string | null; language: string | null; nickname: string | null; total_time_ms: number | null }
        Insert: { build_version?: string | null; country_code?: string | null; finished_at?: string | null; id?: string | null; language?: string | null; nickname?: string | null; total_time_ms?: number | null }
        Update: { build_version?: string | null; country_code?: string | null; finished_at?: string | null; id?: string | null; language?: string | null; nickname?: string | null; total_time_ms?: number | null }
        Relationships: [{ foreignKeyName: "dont100_public_leaderboard_run_id_fkey"; columns: ["id"]; isOneToOne: true; referencedRelation: "dont100_runs"; referencedColumns: ["id"] }]
      }
    }
    Functions: { [_ in never]: never }
    Enums: { [_ in never]: never }
    CompositeTypes: { [_ in never]: never }
  }
}

export type DatabaseWithoutInternals = Omit<Database, "__InternalSupabase">
export type DefaultSchema = DatabaseWithoutInternals[Extract<keyof Database, "public">]
