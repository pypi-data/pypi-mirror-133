export type FactOut = {
  header: {
    id: string;
    ns: string;
    meta: { _ts: number; _ser: number; source: string };
    type: string;
    aggIds: string[];
    version: number;
  };
  payload: Record<string, unknown>;
};
