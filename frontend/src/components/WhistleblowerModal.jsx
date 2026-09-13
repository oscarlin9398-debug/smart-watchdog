import React, { useState } from 'react';
import { AlertCircle, X, CheckCircle2, ShieldAlert, Upload, Send } from 'lucide-react';

export default function WhistleblowerModal({ institutions, onClose, onSubmitReport }) {
  const [targetId, setTargetId] = useState(institutions[0]?.id);
  const [incidentType, setIncidentType] = useState('疑似超額收托與師生比不符');
  const [date, setDate] = useState('2026-09-13');
  const [details, setDetails] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const selectedInst = institutions.find(i => i.id === targetId) || institutions[0];

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!details.trim()) return;

    // Trigger report callback
    onSubmitReport({
      targetId,
      incidentType,
      date,
      details
    });

    setSubmitted(true);
    setTimeout(() => {
      onClose();
    }, 2000);
  };

  return (
    <div className="drawer-backdrop" onClick={onClose} style={{ zIndex: 3000, justifyContent: 'center', alignItems: 'center', padding: '20px' }}>
      <div
        className="glass-panel"
        onClick={(e) => e.stopPropagation()}
        style={{
          width: '580px',
          maxWidth: '100%',
          background: '#ffffff',
          borderRadius: 'var(--radius-md)',
          padding: '28px',
          boxShadow: 'var(--shadow-modal)',
          border: '1px solid #e2e8f0',
          position: 'relative'
        }}
      >
        <button
          onClick={onClose}
          style={{
            position: 'absolute',
            right: '20px',
            top: '20px',
            background: '#f1f5f9',
            border: '1px solid #e2e8f0',
            borderRadius: '50%',
            width: '32px',
            height: '32px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#64748b',
            cursor: 'pointer'
          }}
        >
          <X size={18} />
        </button>

        {submitted ? (
          <div style={{ textAlign: 'center', padding: '36px 0' }}>
            <CheckCircle2 size={54} color="#059669" style={{ margin: '0 auto 16px' }} />
            <h3 style={{ fontSize: '1.25rem', fontWeight: '800', color: '#0f172a', marginBottom: '8px' }}>
              通報已受理並即時連動加權
            </h3>
            <p style={{ fontSize: '0.86rem', color: '#475569', lineHeight: 1.6 }}>
              感謝您的公民監督！該園所【{selectedInst.name}】之風險指標已動態增提權重，並排入本週督學不定期抽檢優先清單。
            </p>
          </div>
        ) : (
          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <div style={{ width: '38px', height: '38px', borderRadius: '10px', background: '#fff1f2', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#e11d48' }}>
                <AlertCircle size={22} />
              </div>
              <div>
                <h3 style={{ fontSize: '1.15rem', fontWeight: '800', color: '#0f172a' }}>
                  公民異常案件舉報沙盒
                </h3>
                <p style={{ fontSize: '0.76rem', color: '#64748b' }}>
                  通報內容將即時啟動風險動態模擬，並通知權責機關
                </p>
              </div>
            </div>

            <div>
              <label style={{ fontSize: '0.8rem', fontWeight: '700', color: '#334155', display: 'block', marginBottom: '6px' }}>
                被檢舉園所名稱
              </label>
              <select
                className="filter-select"
                style={{ width: '100%', borderColor: '#cbd5e1' }}
                value={targetId}
                onChange={(e) => setTargetId(e.target.value)}
              >
                {institutions.map(inst => (
                  <option key={inst.id} value={inst.id}>
                    [{inst.city} {inst.district}] {inst.name}
                  </option>
                ))}
              </select>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
              <div>
                <label style={{ fontSize: '0.8rem', fontWeight: '700', color: '#334155', display: 'block', marginBottom: '6px' }}>
                  異常違法類型
                </label>
                <select
                  className="filter-select"
                  style={{ width: '100%', borderColor: '#cbd5e1' }}
                  value={incidentType}
                  onChange={(e) => setIncidentType(e.target.value)}
                >
                  <option value="疑似超額收托與師生比不符">疑似超額收托與師生比不符</option>
                  <option value="不當管教或情緒語言">不當管教或情緒語言</option>
                  <option value="未聘具合格教保資格師資">未聘具合格教保資格師資</option>
                  <option value="擅自收取未核備代辦才藝費">擅自收取未核備代辦才藝費</option>
                  <option value="幼童專用車超載或改裝">幼童專用車超載或改裝</option>
                  <option value="餐點縮水或衛生有異味">餐點縮水或衛生有異味</option>
                </select>
              </div>
              <div>
                <label style={{ fontSize: '0.8rem', fontWeight: '700', color: '#334155', display: 'block', marginBottom: '6px' }}>
                  發現或事發日期
                </label>
                <input
                  type="date"
                  className="search-input"
                  style={{ width: '100%', padding: '8px 12px' }}
                  value={date}
                  onChange={(e) => setDate(e.target.value)}
                />
              </div>
            </div>

            <div>
              <label style={{ fontSize: '0.8rem', fontWeight: '700', color: '#334155', display: 'block', marginBottom: '6px' }}>
                具體事證與情節陳述
              </label>
              <textarea
                className="search-input"
                style={{ width: '100%', minHeight: '90px', resize: 'vertical', lineHeight: 1.5 }}
                placeholder="請具體敘述班級名稱、違規時間、是否有私立外聘老師或地下室活動等情事..."
                value={details}
                onChange={(e) => setDetails(e.target.value)}
                required
              />
            </div>

            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px', marginTop: '10px' }}>
              <button
                type="button"
                onClick={onClose}
                style={{
                  padding: '9px 18px',
                  borderRadius: 'var(--radius-sm)',
                  background: '#f1f5f9',
                  border: '1px solid #cbd5e1',
                  color: '#475569',
                  fontSize: '0.84rem',
                  fontWeight: '700',
                  cursor: 'pointer'
                }}
              >
                取消
              </button>
              <button
                type="submit"
                style={{
                  padding: '9px 22px',
                  borderRadius: 'var(--radius-sm)',
                  background: '#e11d48',
                  border: 'none',
                  color: '#ffffff',
                  fontSize: '0.84rem',
                  fontWeight: '700',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  boxShadow: '0 2px 8px rgba(225, 29, 72, 0.25)'
                }}
              >
                <Send size={15} /> 提交事證並重算權重
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}
