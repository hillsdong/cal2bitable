'use client'
import { useState, useEffect } from 'react';
import { bitable } from '@base-open/connector-api';
import styles from './index.module.css';


export default function App() {
  const [caldavURL, setCaldavURL] = useState('');
  const [caldavUser, setCaldavUser] = useState('');
  const [caldavPass, setCaldavPass] = useState('');
  const [userId, setUserId] = useState('');
  const [tenantKey, setTenantKey] = useState('');
  useEffect(() => {
    bitable.getConfig().then(config => {
      console.log('config:', config);
      setCaldavURL(config?.caldavURL || '');
      setCaldavUser(config?.caldavUser || '');
      setCaldavPass(config?.caldavPass || '');
    });
    bitable.getUserId().then(id => {
      setUserId(id);
    });
    bitable.getTenantKey().then(key => {
      setTenantKey(key);
    })
  }, [])
  return (
    <div >
      <div className={styles.row}>
        <div className={styles.label}>Caldav 地址:  </div>
        <input className={styles.input} value={caldavURL} onChange={(e) => { setCaldavURL(e.target.value) }} />
      </div>
      <div className={styles.row}>
        <div className={styles.label}>Caldav 用户:</div>
        <input className={styles.input} value={caldavUser} onChange={(e) => { setCaldavUser(e.target.value) }} />
      </div>
      <div className={styles.row}>
        <div className={styles.label}>Caldav 密码: </div>
        <input className={styles.input} type="password" value={caldavPass} onChange={(e) => { setCaldavPass(e.target.value) }} />
      </div>
      <div className={styles.row}>
        <button className={styles.button} onClick={() => {
          bitable.saveConfigAndGoNext({ caldavURL, caldavUser, caldavPass, key: userId })
        }}>下一步</button>
      </div>
    </div>
  )
}