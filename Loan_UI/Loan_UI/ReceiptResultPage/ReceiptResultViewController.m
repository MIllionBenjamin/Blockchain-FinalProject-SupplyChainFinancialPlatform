//
//  UICollectionViewController+ReceiptResultViewController.m
//  Loan_UI
//
//  Created by MillionBenjamin on 2019/12/13.
//  Copyright © 2019 中山大学. All rights reserved.
//

#import "ReceiptResultViewController.h"
#import "AppDelegate.h"
#import "Masonry.h"

@interface ReceiptResultViewController ()<UICollectionViewDataSource,UICollectionViewDelegate>
{
    UICollectionView *mainCollectionView;
    NSArray* array;
}

@end

@implementation ReceiptResultViewController

- (void)initWithArrar:(NSArray *)dic {
    array = dic;
    NSLog(@"%@", array);
}

- (void)viewDidLoad {
    [super viewDidLoad];
    
    UICollectionViewFlowLayout *layout = [[UICollectionViewFlowLayout alloc] init];
    layout.headerReferenceSize = CGSizeMake(self.view.frame.size.width, 40);
    //该方法也可以设置itemSize
    layout.itemSize =CGSizeMake(self.view.frame.size.width, self.view.frame.size.height / 2);
    mainCollectionView = [[UICollectionView alloc] initWithFrame:self.view.bounds collectionViewLayout:layout];
    [self.view addSubview:mainCollectionView];
    
    //NSLog(@"%f, %f", mainCollectionView.frame.size.width, mainCollectionView.frame.size.height);
    
    
    mainCollectionView.frame = CGRectMake(0, 80, self.view.frame.size.width, self.view.frame.size.height);
    
    mainCollectionView.backgroundColor = [UIColor clearColor];
    [mainCollectionView registerClass:[ReceiptResultCollectiionViewCell class] forCellWithReuseIdentifier:@"cellId"];
    [mainCollectionView registerClass:[UICollectionReusableView class] forSupplementaryViewOfKind:UICollectionElementKindSectionHeader withReuseIdentifier:@"reusableView"];
       
       //4.设置代理
    mainCollectionView.delegate = self;
    mainCollectionView.dataSource = self;
    
    /*
    UIEdgeInsets inset_collection = UIEdgeInsetsMake(340, 100, 300, 100);
    
    [mainCollectionView mas_makeConstraints:^(MASConstraintMaker *make){
        make.edges.equalTo(self.view).with.insets(inset_collection);
    }];
     */
    
    
}

- (NSInteger)numberOfSectionsInCollectionView:(UICollectionView *)collectionView
{
    return array.count;
}

- (NSInteger)collectionView:(nonnull UICollectionView *)collectionView numberOfItemsInSection:(NSInteger)section {
    return 1;
}

- (UICollectionViewCell *)collectionView:(UICollectionView *)collectionView cellForItemAtIndexPath:(NSIndexPath *)indexPath
{

    ReceiptResultCollectiionViewCell *cell = (ReceiptResultCollectiionViewCell *)[collectionView dequeueReusableCellWithReuseIdentifier:@"cellId" forIndexPath:indexPath];
    
    //[cell.UnitButton setTitle:[NSString stringWithFormat:@"Unit %ld",(long)indexPath.section + 1] forState:0];
    [cell.item1 setText:[NSString stringWithFormat:@"给出方 ：%@", array[indexPath.section][@"Name_A"]]];
    [cell.item2 setText:[NSString stringWithFormat:@"接收方 ：%@", array[indexPath.section][@"Name_B"]]];
    [cell.item3 setText:[NSString stringWithFormat:@"资产数额：%@", array[indexPath.section][@"amount"]]];
    
    if([array[indexPath.section][@"bankParticipation"] integerValue] == 1) {
        [cell.item4 setText:@"银行参与：是"];
    }
    else {
        [cell.item4 setText:@"银行参与：否"];
    }
    
    if([array[indexPath.section][@"isRealMoney"] integerValue] == 1) {
        [cell.item4 setText:@"真实资金：是"];
    }
    else {
        [cell.item4 setText:@"真实资金：否"];
    }
    
    return cell;
}
/*
- (CGSize)collectionView:(UICollectionView *)collectionView layout:(UICollectionViewLayout *)collectionViewLayout referenceSizeForFooterInSection:(NSInteger)section
{
    return CGSizeMake(10, 10);
}
*/
/*
- (CGFloat)collectionView:(UICollectionView *)collectionView layout:(UICollectionViewLayout *)collectionViewLayout minimumLineSpacingForSectionAtIndex:(NSInteger)section
{
    return 20;
}
*/

-(UIEdgeInsets)collectionView:(UICollectionView *)collectionView layout:(UICollectionViewLayout *)collectionViewLayout insetForSectionAtIndex:(NSInteger)section
{
    return UIEdgeInsetsMake(10, 10, 0, 10);//分别为上、左、下、右
}

-(CGSize)collectionView:(UICollectionView *)collectionView layout:(UICollectionViewLayout*)collectionViewLayout sizeForItemAtIndexPath:(NSIndexPath*)indexPath{
    return CGSizeMake(self.view.frame.size.width, self.view.frame.size.height / 5);
}


- (UICollectionReusableView *)collectionView:(UICollectionView *)collectionView viewForSupplementaryElementOfKind:(NSString *)kind atIndexPath:(NSIndexPath *)indexPath
{
    UICollectionReusableView *headerView = [collectionView dequeueReusableSupplementaryViewOfKind:UICollectionElementKindSectionHeader withReuseIdentifier:@"reusableView" forIndexPath:indexPath];
    headerView.backgroundColor =[UIColor systemBlueColor];
    UILabel *label = [[UILabel alloc] initWithFrame:CGRectMake(20, 0, headerView.frame.size.width, headerView.frame.size.height)];
    label.text = [NSString stringWithFormat:@"%ld", indexPath.section + 1];
    label.font = [UIFont systemFontOfSize:20];
    [headerView addSubview:label];
    return headerView;
}


@end

