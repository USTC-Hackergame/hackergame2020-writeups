import React, { useCallback, useEffect, useMemo, useState } from 'react';
import Axios from 'axios';
import { Button, Card, Descriptions, Form, InputNumber, Layout, Modal, Select, Spin, Table } from 'antd';

import './style.css';
import Coin from './coin.png';


function account_name({ type, id }) {
  return {debit: '储蓄卡', credit: '信用卡'}[type] + ' ' + id;
}

function account_balance_name({ type }) {
  return {debit: '余额', credit: '欠款'}[type];
}

function account_daily_interest({ type, balance }) {
  if (type === 'debit') {
    return Math.round(balance * 0.003);
  }
  if (type === 'credit') {
    return balance ? Math.max(10, Math.round(balance * 0.005)) : 0;
  }
}

function account_interest_text({ type }) {
  return {
    debit: <span>每日 <span className='amount-raw'>0.3%</span></span>,
    credit: <span>每日 <span className='amount-raw'>0.5%</span>，最低 <Amount value={10} /></span>,
  }[type];
}

function Amount({ value, suffix, ...props }) {
  return (
    <span className='amount' {...props}>
      {value}
      <img src={Coin} />
    </span>
  );
}

function Account({ account, ...props }) {
  return (
    <Card
      className={`account account-${account.type}`}
      size='small'
      hoverable
      title={account_name(account)}
      {...props}
    >
      <div className='split'>
        <span>{account_balance_name(account)}</span>
        <Amount value={account.balance} />
      </div>
    </Card>
  );
}

function useTransferForm({ accounts, onSubmit }) {
  const [visible, setVisible] = useState(false);
  const [form] = Form.useForm();
  function show() {
    setVisible(true);
  }
  function onCancel() {
    setVisible(false);
  }
  function onOk() {
    form.validateFields().then(v => {
      form.resetFields();
      setVisible(false);
      onSubmit(v);
    }).catch(e => { console.log(e); });
  }
  if (accounts === undefined) {
    return [null, show];
  }
  const node = (
    <Modal visible={visible} title='转账' onCancel={onCancel} onOk={onOk}>
      <Form form={form}>
        <Form.Item
          name='src'
          label='付款卡'
          rules={[{ required: true, message: '请选择付款卡' }]}
        >
          <Select allowClear showSearch optionFilterProp='children'>
            {accounts.map(i => (
              <Select.Option key={i.id} value={i.id}>{account_name(i)}</Select.Option>
            ))}
          </Select>
        </Form.Item>
        <Form.Item
          name='dst'
          label='收款卡'
          rules={[{ required: true, message: '请选择收款卡' }]}
        >
          <Select allowClear showSearch optionFilterProp='children'>
            {accounts.map(i => (
              <Select.Option key={i.id} value={i.id}>{account_name(i)}</Select.Option>
            ))}
          </Select>
        </Form.Item>
        <Form.Item
          name='amount'
          label='数额'
          rules={[
            { required: true, message: '请填写数额' },
            { type: 'number', min: 1, message: '数额至少为 1' },
          ]}
        >
          <InputNumber allowClear precision={0} min={0} step={100} />
        </Form.Item>
      </Form>
    </Modal>
  );
  return [node, show];
}

function Content({ account, transactions, showTransferForm, newAccount, nextDay }) {
  if (!account) {
    return <>
      <Card
        title='狗狗银行储蓄卡'
        extra={<Button type='primary' onClick={() => newAccount('debit')}>办卡</Button>}
        style={{ margin: '24px' }}
      >
        <p>灵活理财，就办狗狗银行储蓄卡！</p>
      </Card>
      <Card
        title='狗狗银行信用卡'
        extra={<Button type='primary' onClick={() => newAccount('credit')}>办卡</Button>}
        style={{ margin: '24px' }}
      >
        <p>无抵押，无担保，额度高，利率低</p>
        <p>无需提供身份证，最快下款一秒种</p>
        <p>急用钱？就办狗狗银行信用卡！</p>
      </Card>
    </>;
  }

  const columns = [
    { title: '日期', dataIndex: 'date', key: 'date', align: 'center' },
    { title: '类型', dataIndex: 'description', key: 'description' },
    { title: '交易额', dataIndex: 'change', key: 'change', align: 'right', render: v => <Amount value={v} /> },
    { title: account_balance_name(account), dataIndex: 'balance', key: 'balance', align: 'right', render: v => <Amount value={v} /> },
  ];

  return <>
    <Card style={{ margin: '24px' }}>
      <Descriptions
        column={2}
        title={account_name(account)}
        extra={<Button type='primary' onClick={showTransferForm}>转账</Button>}
      >
        <Descriptions.Item label={account_balance_name(account)}>
          <Amount value={account.balance} />
        </Descriptions.Item>
        <Descriptions.Item label='每日利息'>
          <Amount value={account_daily_interest(account)} />
        </Descriptions.Item>
        <Descriptions.Item label='利率' span={2}>
          {account_interest_text(account)}
        </Descriptions.Item>
      </Descriptions>
    </Card>
    <Card style={{ margin: '24px' }}>
      <Form layout='inline' onFinish={() => nextDay(account.id)}>
        <span>用这张卡花费 <Amount value={10} /> 吃饭并结束一天</span>
        <Button
          type='primary'
          htmlType='submit'
          style={{ position: 'absolute', top: '22px', right: '22px' }}
        >
          确认
        </Button>
      </Form>
    </Card>
    <Card style={{ margin: '24px' }}>
      {transactions ? (
        <Table columns={columns} dataSource={transactions.slice().reverse()} rowKey='id' />
      ) : (
        <Table columns={columns} loading />
      )}
    </Card>
  </>;
}

export default function App({ token }) {
  const [accounts, setAccounts] = useState(undefined);
  const [flag, setFlag] = useState(null);
  const [accountId, setAccountId] = useState(1);
  const [transactions, setTransactions] = useState(undefined);
  const axios = useMemo(() => Axios.create({
    baseURL: '/api',
    timeout: 10000,
    headers: { Authorization: `Bearer ${token}` },
  }), [token]);
  const loadTransactions = useCallback(() => {
    setTransactions(undefined);
    if (accountId !== null) {
      axios.get('/transactions', {
        params: { account: accountId },
      }).then(({ data: { transactions } }) => {
        setTransactions(transactions);
      }).catch(e => {
        console.log(e);
        try { alert(e.response.data.errors.join('\n')); }
        catch {}
        setTransactions(null);
      });
    }
  }, [axios, accountId]);
  const loadAccounts = useCallback(() => {
    setAccounts(undefined);
    axios.get('/user').then(({ data: { accounts, flag } }) => {
      setAccounts(accounts);
      if (flag) {
        setFlag(flag);
      }
    }).catch(e => {
      console.log(e);
      try { alert(e.response.data.errors.join('\n')); }
      catch {}
      alert('加载失败');
    });
    loadTransactions();
  }, [axios, loadTransactions]);
  useEffect(loadAccounts, [loadAccounts]);
  const [transferForm, showTransferForm] = useTransferForm({
    accounts,
    onSubmit(v) {
      axios.post('/transfer', v).catch(e => {
        console.log(e);
        try { alert(e.response.data.errors.join('\n')); }
        catch {}
      }).then(loadAccounts);
    },
  })

  if (accounts === undefined) {
    return (
      <div className='center' style={{ height: '100vh' }}>
        <Spin size='large' />
      </div>
    );
  }

  const assets = accounts.filter(i => i.type === 'debit').map(i => i.balance).reduce((a, b) => a + b, 0);
  const liabilities = accounts.filter(i => i.type === 'credit').map(i => i.balance).reduce((a, b) => a + b, 0);
  const equity = assets - liabilities;

  return (
    <Layout style={{ alignItems: 'center' }}>
      <Layout.Content>
        <Layout style={{ height: '100vh', width: '100vw', maxWidth: '1000px' }}>
          <Layout.Sider className='sider' theme='light' width={250}>
            <Card>
              <h1>狗狗银行</h1>
              <div className='split'>
                <span>资产</span>
                <Amount value={assets} />
              </div>
              <div className='split'>
                <span>负债</span>
                <Amount value={liabilities} />
              </div>
              <div className='split'>
                <span>净资产</span>
                <Amount value={equity} />
              </div>
              <div style={{ textAlign: 'right' }}>
                净资产高于 2000 时获胜
                <Button type='primary' onClick={() => {
                  axios.post('/reset', {}).then(() => {
                    setAccountId(1);
                  }).catch(e => {
                    console.log(e);
                    try { alert(e.response.data.errors.join('\n')); }
                    catch {}
                  }).then(loadAccounts);
                  // FIXME: setAccountId 没更新 loadAccounts，导致加载错误的记录
                }}>重新开始</Button>
              </div>
              {flag ? <div>{flag}</div> : null}
            </Card>
            {accounts.map(i => (
              <Account key={i.id} account={i} onClick={() => setAccountId(i.id)}/>
            ))}
            <Card className='new-account' hoverable onClick={() => setAccountId(null)}>
              办新卡
            </Card>
          </Layout.Sider>
          <Layout.Content>
            <Content
              account={accounts.find(i => i.id === accountId)}
              transactions={transactions}
              showTransferForm={showTransferForm}
              newAccount={type => {
                axios.post('/create', { type }).catch(e => {
                  console.log(e);
                  try { alert(e.response.data.errors.join('\n')); }
                  catch {}
                }).then(loadAccounts);
              }}
              nextDay={account => {
                axios.post('/eat', { account }).catch(e => {
                  console.log(e);
                  try { alert(e.response.data.errors.join('\n')); }
                  catch {}
                }).then(loadAccounts);
              }}
            />
            {transferForm}
          </Layout.Content>
        </Layout>
      </Layout.Content>
    </Layout>
  );
};
