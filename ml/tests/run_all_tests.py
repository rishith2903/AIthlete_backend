#!/usr/bin/env python3
"""
Master Test Runner for All 4 AI Fitness Models
Executes comprehensive test suites for all models and generates final report
"""

import sys
import os
import json
import subprocess
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def run_test_suite(test_file, model_name):
    """Run a specific test suite"""
    print(f"\n{'='*80}")
    print(f"🧪 RUNNING {model_name.upper()} TEST SUITE")
    print(f"{'='*80}")
    
    try:
        # Run the test suite
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"✅ {model_name} test suite completed successfully")
            return True
        else:
            print(f"❌ {model_name} test suite failed")
            print(f"Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {model_name} test suite timed out")
        return False
    except Exception as e:
        print(f"❌ {model_name} test suite error: {e}")
        return False

def collect_test_reports():
    """Collect all test reports"""
    reports = {}
    report_files = [
        'pose_estimation_test_report.json',
        'nutrition_test_report.json', 
        'workout_test_report.json',
        'chatbot_test_report.json'
    ]
    
    for report_file in report_files:
        if os.path.exists(report_file):
            try:
                with open(report_file, 'r') as f:
                    reports[report_file.replace('_test_report.json', '')] = json.load(f)
            except Exception as e:
                print(f"Warning: Could not load {report_file}: {e}")
    
    return reports

def generate_master_report(reports):
    """Generate master test report"""
    print(f"\n{'='*100}")
    print("📊 MASTER TEST REPORT - ALL 4 AI FITNESS MODELS")
    print(f"{'='*100}")
    
    total_tests = 0
    total_passed = 0
    total_failed = 0
    model_results = {}
    
    # Calculate totals
    for model_name, report in reports.items():
        total_tests += report.get('total_tests', 0)
        total_passed += report.get('passed_tests', 0)
        total_failed += report.get('failed_tests', 0)
        model_results[model_name] = {
            'total_tests': report.get('total_tests', 0),
            'passed_tests': report.get('passed_tests', 0),
            'failed_tests': report.get('failed_tests', 0),
            'success_rate': report.get('success_rate', 0)
        }
    
    overall_success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
    
    # Print summary
    print(f"\n📈 OVERALL SUMMARY:")
    print(f"Total Tests Across All Models: {total_tests}")
    print(f"Total Passed: {total_passed} ✅")
    print(f"Total Failed: {total_failed} ❌")
    print(f"Overall Success Rate: {overall_success_rate:.1f}%")
    
    # Print individual model results
    print(f"\n📋 INDIVIDUAL MODEL RESULTS:")
    for model_name, results in model_results.items():
        status = "✅ PASS" if results['success_rate'] >= 85 else "❌ FAIL"
        print(f"{model_name.replace('_', ' ').title():<25} | "
              f"Tests: {results['total_tests']:>3} | "
              f"Passed: {results['passed_tests']:>3} | "
              f"Failed: {results['failed_tests']:>3} | "
              f"Success: {results['success_rate']:>5.1f}% | "
              f"{status}")
    
    # Detailed breakdown
    print(f"\n🔍 DETAILED BREAKDOWN:")
    for model_name, report in reports.items():
        print(f"\n{model_name.replace('_', ' ').title()}:")
        print(f"  Success Rate: {report.get('success_rate', 0):.1f}%")
        
        # Show failed tests if any
        failed_tests = [r for r in report.get('results', []) if r['result'] == 'FAIL']
        if failed_tests:
            print(f"  Failed Tests: {len(failed_tests)}")
            for test in failed_tests[:3]:  # Show first 3 failures
                print(f"    - {test['test_id']}: {test['notes']}")
            if len(failed_tests) > 3:
                print(f"    ... and {len(failed_tests) - 3} more")
        else:
            print(f"  ✅ All tests passed!")
    
    # Quality assessment
    print(f"\n🎯 QUALITY ASSESSMENT:")
    if overall_success_rate >= 95:
        print("🏆 EXCELLENT - All models performing at high quality")
    elif overall_success_rate >= 85:
        print("✅ GOOD - Models ready for production with minor issues")
    elif overall_success_rate >= 70:
        print("⚠️ FAIR - Models need improvement before production")
    else:
        print("❌ POOR - Models require significant fixes")
    
    # Save master report
    master_report = {
        'timestamp': datetime.now().isoformat(),
        'overall_summary': {
            'total_tests': total_tests,
            'total_passed': total_passed,
            'total_failed': total_failed,
            'overall_success_rate': overall_success_rate
        },
        'model_results': model_results,
        'detailed_reports': reports,
        'quality_assessment': {
            'grade': 'EXCELLENT' if overall_success_rate >= 95 else
                    'GOOD' if overall_success_rate >= 85 else
                    'FAIR' if overall_success_rate >= 70 else 'POOR',
            'production_ready': overall_success_rate >= 85
        }
    }
    
    with open('master_test_report.json', 'w') as f:
        json.dump(master_report, f, indent=2)
    
    print(f"\n📄 Master test report saved to: master_test_report.json")
    
    return overall_success_rate >= 85

def main():
    """Run all test suites"""
    print("🧪 MASTER TEST RUNNER - AI FITNESS MODELS")
    print("="*80)
    print("Testing all 4 AI models with comprehensive test suites...")
    
    # Define test suites
    test_suites = [
        ('pose_estimation_tests.py', 'Pose Estimation'),
        ('nutrition_tests.py', 'Nutrition'),
        ('workout_tests.py', 'Workout Recommendation'),
        ('chatbot_tests.py', 'Fitness Chatbot')
    ]
    
    # Run all test suites
    results = {}
    for test_file, model_name in test_suites:
        if os.path.exists(test_file):
            success = run_test_suite(test_file, model_name)
            results[model_name] = success
        else:
            print(f"❌ Test file {test_file} not found")
            results[model_name] = False
    
    # Collect reports and generate master report
    print(f"\n{'='*80}")
    print("📊 COLLECTING TEST REPORTS...")
    print(f"{'='*80}")
    
    reports = collect_test_reports()
    production_ready = generate_master_report(reports)
    
    # Final summary
    print(f"\n{'='*80}")
    print("🎉 TESTING COMPLETE!")
    print(f"{'='*80}")
    
    if production_ready:
        print("✅ ALL MODELS ARE PRODUCTION READY!")
        print("🚀 Your AI fitness system is ready for deployment!")
    else:
        print("⚠️ SOME MODELS NEED IMPROVEMENT")
        print("🔧 Please review the detailed reports and fix issues before deployment")
    
    print(f"\n📁 Test reports generated:")
    for report_file in ['pose_estimation_test_report.json', 'nutrition_test_report.json', 
                       'workout_test_report.json', 'chatbot_test_report.json', 'master_test_report.json']:
        if os.path.exists(report_file):
            print(f"  ✅ {report_file}")
        else:
            print(f"  ❌ {report_file} (missing)")
    
    return production_ready

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
