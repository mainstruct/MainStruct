"""
初始化脚本 - 创建示例数据
"""
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.app.core.database import SessionLocal, init_db
from backend.app.models.models import Topic, Case, StructurePattern


def create_topics(db):
    """创建话题"""
    topics_data = [
        {
            "name": "职场晋升",
            "description": "关于职场晋升、升职加薪、职业发展的问题"
        },
        {
            "name": "消费维权",
            "description": "关于消费者权益保护、商家纠纷、退款退货的问题"
        },
        {
            "name": "商业谈判",
            "description": "关于商业合作、价格谈判、合同协商的问题"
        }
    ]

    topics = []
    for data in topics_data:
        topic = Topic(**data)
        db.add(topic)
        topics.append(topic)

    db.commit()
    print(f"✓ 创建了 {len(topics)} 个话题")
    return topics


def create_cases(db, topics):
    """创建示例案例"""
    # 职场晋升案例
    workplace_cases = [
        {
            "topic_id": topics[0].id,
            "description": "我在公司工作3年，业绩优秀，想申请晋升，但老板总说'再看看'，态度模糊",
            "subject_structure": "++-",
            "object_structure": "-?-",
            "structure_key": "++- vs -?-",
            "intent_time": 7,
            "intent_benefit": 8,
            "intent_risk": 4,
            "outcome": "成功",
            "outcome_description": "通过主动展示成果，明确表达诉求，最终获得晋升",
            "verified": 1
        },
        {
            "topic_id": topics[0].id,
            "description": "想要加薪，但不知道怎么开口，担心被拒绝影响关系",
            "subject_structure": "-+-",
            "object_structure": "++-",
            "structure_key": "-+- vs ++-",
            "intent_time": 5,
            "intent_benefit": 9,
            "intent_risk": 3,
            "outcome": "部分成功",
            "outcome_description": "准备充分数据后提出，获得小幅加薪",
            "verified": 1
        },
        {
            "topic_id": topics[0].id,
            "description": "有同事竞争同一个晋升机会，对方关系更好",
            "subject_structure": "++-",
            "object_structure": "+++",
            "structure_key": "++- vs +++",
            "intent_time": 8,
            "intent_benefit": 9,
            "intent_risk": 6,
            "outcome": "失败",
            "outcome_description": "仅靠业绩不足，需要建立更好的人际关系",
            "verified": 1
        },
        {
            "topic_id": topics[0].id,
            "description": "公司承诺的晋升机会一直拖延，感觉被忽悠",
            "subject_structure": "--+",
            "object_structure": "+-?",
            "structure_key": "--+ vs +-?",
            "intent_time": 9,
            "intent_benefit": 8,
            "intent_risk": 7,
            "outcome": "成功",
            "outcome_description": "准备好后备选择，给出明确期限，最终兑现承诺",
            "verified": 1
        },
        {
            "topic_id": topics[0].id,
            "description": "想转岗到更好的部门，但现任领导不放人",
            "subject_structure": "++-",
            "object_structure": "+--",
            "structure_key": "++- vs +--",
            "intent_time": 6,
            "intent_benefit": 7,
            "intent_risk": 5,
            "outcome": "成功",
            "outcome_description": "通过上级领导协调，找到双赢方案",
            "verified": 1
        },
        {
            "topic_id": topics[0].id,
            "description": "觉得自己能力强但一直得不到重用",
            "subject_structure": "-++",
            "object_structure": "+?-",
            "structure_key": "-++ vs +?-",
            "intent_time": 7,
            "intent_benefit": 8,
            "intent_risk": 4,
            "outcome": "部分成功",
            "outcome_description": "主动申请重要项目，证明能力后获得认可",
            "verified": 1
        },
        {
            "topic_id": topics[0].id,
            "description": "新领导不认可之前的工作成果",
            "subject_structure": "?+-",
            "object_structure": "+-?",
            "structure_key": "?+- vs +-?",
            "intent_time": 8,
            "intent_benefit": 7,
            "intent_risk": 6,
            "outcome": "成功",
            "outcome_description": "重新展示价值，调整工作方式适应新领导",
            "verified": 1
        },
        {
            "topic_id": topics[0].id,
            "description": "想跳槽到竞争对手公司，薪资翻倍但有竞业协议",
            "subject_structure": "++-",
            "object_structure": "+--",
            "structure_key": "++- vs +--",
            "intent_time": 9,
            "intent_benefit": 10,
            "intent_risk": 8,
            "outcome": "成功",
            "outcome_description": "咨询律师确认竞业范围，找到合规岗位",
            "verified": 1
        },
        {
            "topic_id": topics[0].id,
            "description": "公司画大饼承诺期权，但迟迟不兑现",
            "subject_structure": "--?",
            "object_structure": "+-?",
            "structure_key": "--? vs +-?",
            "intent_time": 6,
            "intent_benefit": 9,
            "intent_risk": 5,
            "outcome": "失败",
            "outcome_description": "没有书面协议，无法维权，选择离职",
            "verified": 1
        },
        {
            "topic_id": topics[0].id,
            "description": "想申请远程办公，但公司文化不支持",
            "subject_structure": "++-",
            "object_structure": "---",
            "structure_key": "++- vs ---",
            "intent_time": 5,
            "intent_benefit": 6,
            "intent_risk": 3,
            "outcome": "部分成功",
            "outcome_description": "提出试行方案，获得每周2天远程",
            "verified": 1
        }
    ]

    # 消费维权案例
    consumer_cases = [
        {
            "topic_id": topics[1].id,
            "description": "网购商品有质量问题，商家拒绝退款",
            "subject_structure": "++-",
            "object_structure": "+--",
            "structure_key": "++- vs +--",
            "intent_time": 8,
            "intent_benefit": 7,
            "intent_risk": 3,
            "outcome": "成功",
            "outcome_description": "保留证据，平台投诉，获得全额退款",
            "verified": 1
        },
        {
            "topic_id": topics[1].id,
            "description": "健身房跑路，预付费无法退回",
            "subject_structure": "--+",
            "object_structure": "?--",
            "structure_key": "--+ vs ?--",
            "intent_time": 9,
            "intent_benefit": 8,
            "intent_risk": 5,
            "outcome": "部分成功",
            "outcome_description": "集体维权，通过法律途径追回部分费用",
            "verified": 1
        },
        {
            "topic_id": topics[1].id,
            "description": "餐厅食物有异物，要求赔偿但对方态度恶劣",
            "subject_structure": "++-",
            "object_structure": "+--",
            "structure_key": "++- vs +--",
            "intent_time": 9,
            "intent_benefit": 6,
            "intent_risk": 4,
            "outcome": "成功",
            "outcome_description": "拍照取证，联系市场监管，获得赔偿道歉",
            "verified": 1
        },
        {
            "topic_id": topics[1].id,
            "description": "买的手机是翻新机，商家不承认",
            "subject_structure": "++-",
            "object_structure": "+-?",
            "structure_key": "++- vs +-?",
            "intent_time": 8,
            "intent_benefit": 9,
            "intent_risk": 5,
            "outcome": "成功",
            "outcome_description": "官方鉴定，凭检测报告退货并索赔",
            "verified": 1
        },
        {
            "topic_id": topics[1].id,
            "description": "装修公司偷工减料，拒不整改",
            "subject_structure": "++-",
            "object_structure": "+--",
            "structure_key": "++- vs +--",
            "intent_time": 9,
            "intent_benefit": 10,
            "intent_risk": 7,
            "outcome": "成功",
            "outcome_description": "请第三方检测，走法律程序，获赔并重新施工",
            "verified": 1
        },
        {
            "topic_id": topics[1].id,
            "description": "网课质量差想退款，平台说已过期",
            "subject_structure": "-+-",
            "object_structure": "+-?",
            "structure_key": "-+- vs +-?",
            "intent_time": 6,
            "intent_benefit": 7,
            "intent_risk": 3,
            "outcome": "部分成功",
            "outcome_description": "引用消费者保护法，协商退回70%",
            "verified": 1
        },
        {
            "topic_id": topics[1].id,
            "description": "快递丢失贵重物品，快递公司只赔保价金额",
            "subject_structure": "++-",
            "object_structure": "+?-",
            "structure_key": "++- vs +?-",
            "intent_time": 8,
            "intent_benefit": 9,
            "intent_risk": 4,
            "outcome": "失败",
            "outcome_description": "未保价，按规定只能赔付运费数倍",
            "verified": 1
        },
        {
            "topic_id": topics[1].id,
            "description": "美容院强制推销办卡，想取消",
            "subject_structure": "--+",
            "object_structure": "+-?",
            "structure_key": "--+ vs +-?",
            "intent_time": 9,
            "intent_benefit": 8,
            "intent_risk": 3,
            "outcome": "成功",
            "outcome_description": "消协投诉，引用冷静期规定，全额退款",
            "verified": 1
        },
        {
            "topic_id": topics[1].id,
            "description": "买到假货，商家威胁给差评就起诉",
            "subject_structure": "?+-",
            "object_structure": "+--",
            "structure_key": "?+- vs +--",
            "intent_time": 7,
            "intent_benefit": 6,
            "intent_risk": 6,
            "outcome": "成功",
            "outcome_description": "保留证据，据实评价，商家无法起诉",
            "verified": 1
        },
        {
            "topic_id": topics[1].id,
            "description": "租房中介收了钱不办事",
            "subject_structure": "++-",
            "object_structure": "+-?",
            "structure_key": "++- vs +-?",
            "intent_time": 8,
            "intent_benefit": 7,
            "intent_risk": 4,
            "outcome": "成功",
            "outcome_description": "留存聊天记录，投诉住建部门，追回中介费",
            "verified": 1
        }
    ]

    # 商业谈判案例
    business_cases = [
        {
            "topic_id": topics[2].id,
            "description": "供应商突然提价30%，威胁断货",
            "subject_structure": "--+",
            "object_structure": "++-",
            "structure_key": "--+ vs ++-",
            "intent_time": 9,
            "intent_benefit": 9,
            "intent_risk": 7,
            "outcome": "成功",
            "outcome_description": "寻找备选供应商，谈判降至15%涨幅",
            "verified": 1
        },
        {
            "topic_id": topics[2].id,
            "description": "客户拖欠货款，总说'下周一定付'",
            "subject_structure": "-+-",
            "object_structure": "+-?",
            "structure_key": "-+- vs +-?",
            "intent_time": 9,
            "intent_benefit": 10,
            "intent_risk": 6,
            "outcome": "成功",
            "outcome_description": "停止供货，发律师函，3天内收到款项",
            "verified": 1
        },
        {
            "topic_id": topics[2].id,
            "description": "想拿下大客户，但对方要求压价太多",
            "subject_structure": "++-",
            "object_structure": "++-",
            "structure_key": "++- vs ++-",
            "intent_time": 7,
            "intent_benefit": 9,
            "intent_risk": 5,
            "outcome": "成功",
            "outcome_description": "提供增值服务，调整付款方式，达成合作",
            "verified": 1
        },
        {
            "topic_id": topics[2].id,
            "description": "合作伙伴想修改合同条款，降低我方利润",
            "subject_structure": "++-",
            "object_structure": "+-+",
            "structure_key": "++- vs +-+",
            "intent_time": 8,
            "intent_benefit": 8,
            "intent_risk": 6,
            "outcome": "部分成功",
            "outcome_description": "坚持核心条款，在次要部分让步，维持合作",
            "verified": 1
        },
        {
            "topic_id": topics[2].id,
            "description": "投资人压低估值，但急需资金",
            "subject_structure": "--+",
            "object_structure": "+++",
            "structure_key": "--+ vs +++",
            "intent_time": 9,
            "intent_benefit": 10,
            "intent_risk": 8,
            "outcome": "失败",
            "outcome_description": "过于被动，接受不利条款，后悔",
            "verified": 1
        },
        {
            "topic_id": topics[2].id,
            "description": "渠道商要求独家代理，但条件苛刻",
            "subject_structure": "++-",
            "object_structure": "++-",
            "structure_key": "++- vs ++-",
            "intent_time": 6,
            "intent_benefit": 8,
            "intent_risk": 5,
            "outcome": "成功",
            "outcome_description": "提出区域独家+业绩考核，双方满意",
            "verified": 1
        },
        {
            "topic_id": topics[2].id,
            "description": "技术合作方想要更多股权",
            "subject_structure": "++-",
            "object_structure": "+++",
            "structure_key": "++- vs +++",
            "intent_time": 7,
            "intent_benefit": 9,
            "intent_risk": 6,
            "outcome": "成功",
            "outcome_description": "用期权替代股权，设置兑现条件",
            "verified": 1
        },
        {
            "topic_id": topics[2].id,
            "description": "竞争对手恶意竞价，抢走客户",
            "subject_structure": "?+-",
            "object_structure": "++-",
            "structure_key": "?+- vs ++-",
            "intent_time": 9,
            "intent_benefit": 9,
            "intent_risk": 7,
            "outcome": "部分成功",
            "outcome_description": "强调服务优势，保住核心客户，放弃小客户",
            "verified": 1
        },
        {
            "topic_id": topics[2].id,
            "description": "要和前员工签竞业协议，对方要高额补偿",
            "subject_structure": "++-",
            "object_structure": "++-",
            "structure_key": "++- vs ++-",
            "intent_time": 6,
            "intent_benefit": 7,
            "intent_risk": 4,
            "outcome": "成功",
            "outcome_description": "按法律标准补偿，缩小竞业范围",
            "verified": 1
        },
        {
            "topic_id": topics[2].id,
            "description": "广告公司效果不达标，要求退款",
            "subject_structure": "++-",
            "object_structure": "+-?",
            "structure_key": "++- vs +-?",
            "intent_time": 8,
            "intent_benefit": 8,
            "intent_risk": 5,
            "outcome": "成功",
            "outcome_description": "拿出数据对比，协商退50%并重新执行",
            "verified": 1
        }
    ]

    all_cases = workplace_cases + consumer_cases + business_cases

    for case_data in all_cases:
        case = Case(**case_data)
        db.add(case)

    db.commit()
    print(f"✓ 创建了 {len(all_cases)} 个案例")
    return all_cases


def create_patterns(db, topics):
    """创建结构辞（策略模式）"""

    # 基于案例数据生成结构辞
    patterns_data = [
        # 职场晋升相关
        {
            "topic_id": topics[0].id,
            "structure_key": "++- vs -?-",
            "strategy": "主动展示成果，明确表达诉求，设定期限。准备好量化数据证明价值。",
            "reasoning": "主体主动强势但态度不够积极，客体被动且态度消极模糊。需要用事实和数据打消对方疑虑。",
            "success_count": 3,
            "failure_count": 1,
            "success_rate": 0.75,
            "risk_warning": "避免过于激进，给对方思考时间",
            "avg_intent_time": 7.0,
            "avg_intent_benefit": 8.0,
            "avg_intent_risk": 4.0
        },
        {
            "topic_id": topics[0].id,
            "structure_key": "-+- vs ++-",
            "strategy": "充分准备数据和理由，选择合适时机，以请教姿态沟通。",
            "reasoning": "主体被动但有能力，客体主动强势。需要展示价值同时保持谦逊。",
            "success_count": 2,
            "failure_count": 1,
            "success_rate": 0.67,
            "risk_warning": "不要在对方忙碌或心情不好时提出",
            "avg_intent_time": 5.0,
            "avg_intent_benefit": 9.0,
            "avg_intent_risk": 3.0
        },
        {
            "topic_id": topics[0].id,
            "structure_key": "--+ vs +-?",
            "strategy": "准备好后备选择（BATNA），设定明确期限，表明底线。",
            "reasoning": "主体处于弱势但态度积极，需要增强谈判筹码。",
            "success_count": 2,
            "failure_count": 0,
            "success_rate": 1.0,
            "risk_warning": "确保后备选择真实可行，不要虚张声势",
            "avg_intent_time": 8.5,
            "avg_intent_benefit": 8.0,
            "avg_intent_risk": 6.5
        },

        # 消费维权相关
        {
            "topic_id": topics[1].id,
            "structure_key": "++- vs +--",
            "strategy": "保留所有证据（截图、录音、实物），向平台投诉或联系监管部门。",
            "reasoning": "主体主动强势，客体虽主动但能力弱态度差。用规则和证据压制。",
            "success_count": 6,
            "failure_count": 1,
            "success_rate": 0.86,
            "risk_warning": "注意证据的完整性和时效性",
            "avg_intent_time": 8.5,
            "avg_intent_benefit": 7.8,
            "avg_intent_risk": 4.2
        },
        {
            "topic_id": topics[1].id,
            "structure_key": "--+ vs ?--",
            "strategy": "集体维权，寻找更多受害者，走法律途径。",
            "reasoning": "主体弱势，客体更弱但状态不明。人多力量大。",
            "success_count": 1,
            "failure_count": 0,
            "success_rate": 1.0,
            "risk_warning": "法律程序耗时长，要有心理准备",
            "avg_intent_time": 9.0,
            "avg_intent_benefit": 8.0,
            "avg_intent_risk": 5.0
        },

        # 商业谈判相关
        {
            "topic_id": topics[2].id,
            "structure_key": "--+ vs ++-",
            "strategy": "寻找备选方案增强筹码，分析对方真实需求，寻找双赢点。",
            "reasoning": "主体弱势面对强势对手，需要改变力量对比。",
            "success_count": 1,
            "failure_count": 1,
            "success_rate": 0.5,
            "risk_warning": "不要表现出过分焦虑，保持冷静专业",
            "avg_intent_time": 9.0,
            "avg_intent_benefit": 9.5,
            "avg_intent_risk": 7.5
        },
        {
            "topic_id": topics[2].id,
            "structure_key": "++- vs ++-",
            "strategy": "寻找创造性解决方案，在非核心问题上让步，坚持核心利益。",
            "reasoning": "双方势均力敌，需要合作而非对抗。",
            "success_count": 4,
            "failure_count": 0,
            "success_rate": 1.0,
            "risk_warning": "明确区分核心和非核心利益",
            "avg_intent_time": 6.8,
            "avg_intent_benefit": 8.3,
            "avg_intent_risk": 5.3
        },
        {
            "topic_id": topics[2].id,
            "structure_key": "-+- vs +-?",
            "strategy": "采取强硬措施（停止供货、法律手段），明确后果。",
            "reasoning": "主体有能力但被动，需要主动出击。",
            "success_count": 2,
            "failure_count": 0,
            "success_rate": 1.0,
            "risk_warning": "确保措施合法合规，留有余地",
            "avg_intent_time": 8.5,
            "avg_intent_benefit": 9.0,
            "avg_intent_risk": 5.0
        }
    ]

    for pattern_data in patterns_data:
        pattern = StructurePattern(**pattern_data)
        db.add(pattern)

    db.commit()
    print(f"✓ 创建了 {len(patterns_data)} 个结构辞")


def main():
    """主函数"""
    print("开始初始化数据库...\n")

    # 初始化数据库
    init_db()
    print("✓ 数据库表已创建\n")

    # 创建会话
    db = SessionLocal()

    try:
        # 检查是否已有数据
        existing_topics = db.query(Topic).count()
        if existing_topics > 0:
            print(f"⚠ 数据库中已有 {existing_topics} 个话题")
            response = input("是否清空并重新初始化? (yes/no): ")
            if response.lower() != 'yes':
                print("取消初始化")
                return

            # 清空数据
            db.query(Topic).delete()
            db.query(Case).delete()
            db.query(StructurePattern).delete()
            db.commit()
            print("✓ 已清空现有数据\n")

        # 创建数据
        print("创建示例数据...")
        topics = create_topics(db)
        cases = create_cases(db, topics)
        create_patterns(db, topics)

        print("\n" + "="*50)
        print("✅ 初始化完成!")
        print("="*50)
        print(f"话题数: {len(topics)}")
        print(f"案例数: {len(cases)}")
        print("\n现在可以启动应用:")
        print("  后端: cd backend && uvicorn app.main:app --reload")
        print("  前端: cd frontend && streamlit run app.py")

    except Exception as e:
        print(f"\n❌ 初始化失败: {str(e)}")
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()
